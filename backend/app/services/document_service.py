import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.schema import Document

from app.config import settings


class DocumentService:
    """Service for loading and processing resume documents"""

    def __init__(self):
        self.resume_dir = settings.RESUME_DIR
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", ".", " ", ""]
        )

    def _get_loader(self, file_path: str):
        """Get appropriate loader based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return PyPDFLoader(file_path)
        elif ext == ".txt":
            return TextLoader(file_path, encoding="utf-8")
        elif ext in [".md", ".markdown"]:
            return UnstructuredMarkdownLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def load_documents(self) -> List[Document]:
        """Load all documents from the resume directory"""
        documents = []

        if not os.path.exists(self.resume_dir):
            os.makedirs(self.resume_dir)
            print(f"Created resume directory: {self.resume_dir}")
            return documents

        supported_extensions = [".pdf", ".txt", ".md", ".markdown"]

        for filename in os.listdir(self.resume_dir):
            file_path = os.path.join(self.resume_dir, filename)

            if not os.path.isfile(file_path):
                continue

            ext = os.path.splitext(filename)[1].lower()
            if ext not in supported_extensions:
                continue

            try:
                loader = self._get_loader(file_path)
                docs = loader.load()

                # Add metadata
                for doc in docs:
                    doc.metadata["source"] = filename
                    doc.metadata["file_type"] = ext

                documents.extend(docs)
                print(f"✅ Loaded: {filename} ({len(docs)} pages/sections)")

            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks for embedding"""
        if not documents:
            return []

        chunks = self.text_splitter.split_documents(documents)
        print(f"📄 Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks

    def load_and_split(self) -> List[Document]:
        """Load documents and split them into chunks"""
        documents = self.load_documents()
        return self.split_documents(documents)

    def get_document_count(self) -> int:
        """Get count of documents in resume directory"""
        if not os.path.exists(self.resume_dir):
            return 0

        supported_extensions = [".pdf", ".txt", ".md", ".markdown"]
        count = 0

        for filename in os.listdir(self.resume_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in supported_extensions:
                count += 1

        return count

    def list_documents(self) -> List[str]:
        """List all documents in the resume directory"""
        if not os.path.exists(self.resume_dir):
            return []

        supported_extensions = [".pdf", ".txt", ".md", ".markdown"]
        documents = []

        for filename in os.listdir(self.resume_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in supported_extensions:
                documents.append(filename)

        return documents


# Singleton instance
document_service = DocumentService()
