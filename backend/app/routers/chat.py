from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import os
import shutil

from app.config import settings
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ModelsResponse,
    DocumentUploadResponse,
    IndexResponse,
    HealthResponse
)
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.document_service import document_service


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health status of all services"""
    ollama_connected = await llm_service.check_connection()
    stats = rag_service.get_stats()

    return HealthResponse(
        status="healthy" if ollama_connected else "degraded",
        ollama_connected=ollama_connected,
        vectorstore_ready=stats["vectorstore_ready"],
        documents_loaded=stats["documents_count"]
    )


@router.get("/models", response_model=ModelsResponse)
async def list_models():
    """List all available models"""
    models = await llm_service.get_available_models()

    return ModelsResponse(
        models=models,
        default_model=settings.DEFAULT_MODEL
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get a RAG-enhanced response

    The system will:
    1. Search for relevant resume content
    2. Use that content as context for the LLM
    3. Generate a response based on the resume
    """
    try:
        # Use RAG to answer the question
        answer, sources = await rag_service.query(
            question=request.message,
            model=request.model
        )

        return ChatResponse(
            answer=answer,
            model=request.model,
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat response (for real-time output)"""

    async def generate():
        # First, get relevant context
        search_results = await rag_service.search(request.message)

        context_parts = []
        for doc, score in search_results:
            context_parts.append(doc.page_content)

        context = "\n\n---\n\n".join(context_parts) if context_parts else ""

        system_prompt = """You are a helpful assistant that answers questions about a person's resume/CV.
Answer based ONLY on the provided context. If the information is not in the context, say so.
Be concise but informative. Answer in the same language as the question."""

        async for chunk in llm_service.generate_stream(
            prompt=request.message,
            model=request.model,
            system_prompt=system_prompt,
            context=context
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a resume document (PDF, TXT, or Markdown)"""
    # Validate file type
    allowed_extensions = [".pdf", ".txt", ".md", ".markdown"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save file
    file_path = os.path.join(settings.RESUME_DIR, file.filename)

    try:
        os.makedirs(settings.RESUME_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return DocumentUploadResponse(
            filename=file.filename,
            status="success",
            message=f"File uploaded successfully. Run /api/documents/index to update the search index."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")


@router.post("/documents/index", response_model=IndexResponse)
async def index_documents():
    """Re-index all documents in the resume directory"""
    try:
        chunks_indexed = await rag_service.index_documents()

        if chunks_indexed == 0:
            return IndexResponse(
                status="warning",
                documents_indexed=0,
                message="No documents found to index. Please upload documents first."
            )

        return IndexResponse(
            status="success",
            documents_indexed=chunks_indexed,
            message=f"Successfully indexed {chunks_indexed} document chunks."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {e}")


@router.get("/documents")
async def list_documents():
    """List all documents in the resume directory"""
    stats = rag_service.get_stats()

    return {
        "documents": stats["documents"],
        "total_count": stats["documents_count"],
        "chunks_indexed": stats["chunks_count"]
    }
