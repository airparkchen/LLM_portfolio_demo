# Disable ChromaDB telemetry before importing
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import chat
from app.services.rag_service import rag_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    print(f"🚀 Starting {settings.APP_NAME}...")

    # Initialize RAG service (load documents and create vectorstore)
    try:
        await rag_service.initialize()
        print("✅ RAG service initialized")
    except Exception as e:
        print(f"⚠️ RAG service initialization warning: {e}")

    yield

    # Cleanup on shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="A RAG-based resume Q&A system powered by local LLM via Ollama",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/api/health"
    }
