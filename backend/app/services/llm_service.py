import ollama
from typing import List, Optional, AsyncGenerator
import asyncio

from app.config import settings
from app.models.schemas import ModelInfo


class LLMService:
    """Service for interacting with Ollama LLM"""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.DEFAULT_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = ollama.Client(host=self.base_url)
        return self._client

    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.client.list)
            return True
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return False

    async def list_local_models(self) -> List[str]:
        """List all models available locally in Ollama"""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.client.list)
            return [model['name'].split(':')[0] for model in response.get('models', [])]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    async def get_available_models(self) -> List[ModelInfo]:
        """Get list of configured models with availability status"""
        local_models = await self.list_local_models()

        models = []
        for model_config in settings.AVAILABLE_MODELS:
            parts = model_config.split(":")
            name = parts[0]
            display_name = parts[1] if len(parts) > 1 else name
            description = parts[2] if len(parts) > 2 else ""

            models.append(ModelInfo(
                name=name,
                display_name=display_name,
                description=description,
                is_available=name in local_models
            ))

        # Also add any local models not in the config
        for local_model in local_models:
            if not any(m.name == local_model for m in models):
                models.append(ModelInfo(
                    name=local_model,
                    display_name=local_model,
                    description="Custom model",
                    is_available=True
                ))

        return models

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.pull(model_name)
            )
            return True
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Generate a response using the specified model"""
        model = model or self.default_model

        # Build the full prompt with context if provided
        full_prompt = prompt
        if context:
            full_prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {prompt}

Answer:"""

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": full_prompt})

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat(model=model, messages=messages)
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Error generating response with model {model}: {e}")

    async def generate_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response"""
        model = model or self.default_model

        full_prompt = prompt
        if context:
            full_prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {prompt}

Answer:"""

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": full_prompt})

        try:
            stream = self.client.chat(model=model, messages=messages, stream=True)
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
        except Exception as e:
            raise Exception(f"Error in streaming response: {e}")


# Singleton instance
llm_service = LLMService()
