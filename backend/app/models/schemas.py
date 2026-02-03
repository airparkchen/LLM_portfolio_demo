from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's question")
    model: str = Field(default="llama3.2", description="Model to use for generation")
    chat_history: List[ChatMessage] = Field(default=[], description="Previous chat messages for context")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Generated answer")
    model: str = Field(..., description="Model used for generation")
    sources: List[str] = Field(default=[], description="Source documents used")
    timestamp: datetime = Field(default_factory=datetime.now)


class ModelInfo(BaseModel):
    name: str = Field(..., description="Model identifier")
    display_name: str = Field(..., description="Human-readable model name")
    description: str = Field(..., description="Model description")
    is_available: bool = Field(default=False, description="Whether model is currently available")


class ModelsResponse(BaseModel):
    models: List[ModelInfo]
    default_model: str


class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    message: str


class IndexResponse(BaseModel):
    status: str
    documents_indexed: int
    message: str


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    vectorstore_ready: bool
    documents_loaded: int
