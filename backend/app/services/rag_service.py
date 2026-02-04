# Disable ChromaDB telemetry
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

from typing import List, Tuple, Optional
import asyncio
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document

from app.config import settings
from app.services.document_service import document_service
from app.services.llm_service import llm_service


class RAGService:
    """RAG (Retrieval-Augmented Generation) service for resume Q&A"""

    def __init__(self):
        self.vectorstore_dir = settings.VECTORSTORE_DIR
        self.embedding_model = settings.EMBEDDING_MODEL
        self.top_k = settings.TOP_K_RESULTS
        self._vectorstore: Optional[Chroma] = None
        self._embeddings: Optional[OllamaEmbeddings] = None
        self._initialized = False

    @property
    def embeddings(self) -> OllamaEmbeddings:
        """Lazy initialization of embeddings"""
        if self._embeddings is None:
            self._embeddings = OllamaEmbeddings(
                base_url=settings.OLLAMA_BASE_URL,
                model=self.embedding_model
            )
        return self._embeddings

    async def initialize(self) -> bool:
        """Initialize the RAG service"""
        try:
            # Ensure directories exist
            os.makedirs(self.vectorstore_dir, exist_ok=True)
            os.makedirs(settings.RESUME_DIR, exist_ok=True)

            # Check if vectorstore already exists
            if self._check_existing_vectorstore():
                print("📦 Loading existing vectorstore...")
                await self._load_vectorstore()
            else:
                # Try to index documents if any exist
                doc_count = document_service.get_document_count()
                if doc_count > 0:
                    print(f"📄 Found {doc_count} documents, indexing...")
                    await self.index_documents()
                else:
                    print("⚠️ No documents found in resume directory")
                    print(f"   Please add documents to: {settings.RESUME_DIR}")

            self._initialized = True
            return True

        except Exception as e:
            print(f"❌ RAG initialization error: {e}")
            return False

    def _check_existing_vectorstore(self) -> bool:
        """Check if a vectorstore already exists"""
        chroma_dir = os.path.join(self.vectorstore_dir, "chroma.sqlite3")
        return os.path.exists(chroma_dir)

    def _get_chroma_client(self):
        """Get ChromaDB client with telemetry disabled"""
        return chromadb.Client(ChromaSettings(
            anonymized_telemetry=False,
            allow_reset=True
        ))

    async def _load_vectorstore(self):
        """Load existing vectorstore from disk"""
        loop = asyncio.get_event_loop()
        self._vectorstore = await loop.run_in_executor(
            None,
            lambda: Chroma(
                persist_directory=self.vectorstore_dir,
                embedding_function=self.embeddings,
                client_settings=ChromaSettings(anonymized_telemetry=False)
            )
        )

    async def index_documents(self) -> int:
        """Index all documents from the resume directory"""
        # Load and split documents
        chunks = document_service.load_and_split()

        if not chunks:
            print("⚠️ No document chunks to index")
            return 0

        # Create or update vectorstore
        loop = asyncio.get_event_loop()

        print(f"🔄 Creating embeddings for {len(chunks)} chunks...")
        self._vectorstore = await loop.run_in_executor(
            None,
            lambda: Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.vectorstore_dir,
                client_settings=ChromaSettings(anonymized_telemetry=False)
            )
        )

        print(f"✅ Indexed {len(chunks)} chunks")
        return len(chunks)

    async def search(self, query: str, top_k: Optional[int] = None) -> List[Tuple[Document, float]]:
        """Search for relevant documents"""
        if self._vectorstore is None:
            return []

        k = top_k or self.top_k

        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: self._vectorstore.similarity_search_with_score(query, k=k)
        )

        return results

    async def query(
        self,
        question: str,
        model: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> Tuple[str, List[str]]:
        """
        Query the RAG system with a question

        Returns:
            Tuple of (answer, list of source documents)
        """
        # Search for relevant context
        search_results = await self.search(question, top_k)

        sources = []
        context_parts = []

        for doc, score in search_results:
            context_parts.append(doc.page_content)
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)

        context = "\n\n---\n\n".join(context_parts) if context_parts else ""

        # Generate system prompt for resume Q&A
        system_prompt = """You are a helpful assistant that answers questions about a person's resume/CV.
Answer based ONLY on the provided context. If the information is not in the context, say so.
Be concise but informative. Answer in the same language as the question."""

        # Generate response
        if context:
            answer = await llm_service.generate(
                prompt=question,
                model=model,
                system_prompt=system_prompt,
                context=context
            )
        else:
            answer = "I don't have any resume information loaded yet. Please upload a resume document first."

        return answer, sources

    def get_stats(self) -> dict:
        """Get statistics about the RAG system"""
        doc_count = document_service.get_document_count()
        docs = document_service.list_documents()

        chunk_count = 0
        if self._vectorstore is not None:
            try:
                # Get collection count
                chunk_count = self._vectorstore._collection.count()
            except:
                pass

        return {
            "initialized": self._initialized,
            "documents_count": doc_count,
            "documents": docs,
            "chunks_count": chunk_count,
            "vectorstore_ready": self._vectorstore is not None
        }


# Singleton instance
rag_service = RAGService()
