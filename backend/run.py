#!/usr/bin/env python3
"""
Startup script for the LLM RAG Resume System
"""
import uvicorn
import os
import sys


def main():
    # Change to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)

    # Add backend to Python path
    sys.path.insert(0, backend_dir)

    print("=" * 50)
    print("  LLM RAG Resume System")
    print("=" * 50)
    print()
    print("Starting server...")
    print("API Docs: http://localhost:8000/docs")
    print("Health:   http://localhost:8000/api/health")
    print()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
