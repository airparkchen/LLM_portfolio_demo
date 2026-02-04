# LLM RAG Resume System

A local LLM-powered resume Q&A system using Ollama and RAG (Retrieval-Augmented Generation).

<img width="1931" height="1217" alt="llm履歷 (1)" src="https://github.com/user-attachments/assets/440b7a8e-b25f-4551-9d9f-3cdc3bd1d6a7" />

## Features


- **Local LLM Deployment**: Run LLM models locally via Ollama
- **Model Switching**: Switch between different models (Llama 3.2, Mistral, custom GGUF models)
- **RAG System**: Intelligent document retrieval for accurate answers
- **Resume Q&A**: Ask questions about your resume and get contextual answers

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React) - Coming Soon              │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST API
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Chat API   │  │  RAG Engine  │  │  Doc Loader  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Ollama LLM    │  │   ChromaDB      │  │   Resume Files  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Prerequisites

1. **Ollama** - Install from [ollama.ai](https://ollama.ai)
2. **Python 3.10+**

## Quick Start

### 1. Setup Ollama

```bash
# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text  # For embeddings
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 3. Add Your Resume

Place your resume file(s) in `backend/data/resume/`:
- Supported formats: PDF, TXT, Markdown

### 4. Run the Server

```bash
python run.py
```

### 5. Test the API

Open http://localhost:8000/docs for interactive API documentation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/models` | List available models |
| POST | `/api/chat` | Send a question |
| POST | `/api/documents/upload` | Upload a document |
| POST | `/api/documents/index` | Re-index documents |
| GET | `/api/documents` | List indexed documents |

## Using Custom GGUF Models

To use a custom model from Hugging Face:

1. Download the GGUF file
2. Create a Modelfile:
```
FROM /path/to/your/model.gguf
```
3. Create the model in Ollama:
```bash
ollama create custom-model -f Modelfile
```
4. Add to `AVAILABLE_MODELS` in `.env` or use directly in API calls

## Example API Usage

```bash
# Check health
curl http://localhost:8000/api/health

# List models
curl http://localhost:8000/api/models

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your work experience?", "model": "llama3.2"}'
```

## Project Structure

```
LLM_portfolio_demo/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Configuration
│   │   ├── routers/
│   │   │   └── chat.py       # API routes
│   │   ├── services/
│   │   │   ├── llm_service.py      # Ollama integration
│   │   │   ├── rag_service.py      # RAG engine
│   │   │   └── document_service.py # Document processing
│   │   └── models/
│   │       └── schemas.py    # Pydantic models
│   ├── data/
│   │   └── resume/           # Resume files here
│   ├── vectorstore/          # ChromaDB storage
│   ├── requirements.txt
│   └── run.py
├── frontend/                 # Coming soon
└── README.md
```

## License

MIT
