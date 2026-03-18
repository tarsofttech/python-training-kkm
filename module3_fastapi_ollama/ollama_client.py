"""
Ollama Client - Async HTTP client for Ollama API

This module provides an async client for interacting with Ollama's REST API.
It supports both standard and streaming text generation, embeddings, and health checks.
"""

import httpx
from typing import List, Optional, AsyncGenerator
import json


class OllamaConnectionError(Exception):
    """Raised when unable to connect to Ollama."""
    pass


class OllamaClient:
    """
    Async client for Ollama API.
    
    This client handles all communication with the Ollama service,
    including text generation, streaming, embeddings, and health checks.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1",
        embed_model: str = "nomic-embed-text"
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL of the Ollama service
            model: Default model for text generation
            embed_model: Model for generating embeddings
        """
        self.base_url = base_url
        self.model = model
        self.embed_model = embed_model
        self.timeout = 120.0
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Generate text using Ollama (non-streaming).
        
        Args:
            prompt: The text prompt to send to the LLM
            system: Optional system prompt to set behavior
            temperature: Controls randomness (0.0 = deterministic, 2.0 = very random)
            stream: Must be False for this method
        
        Returns:
            str: Generated text
        
        Raises:
            OllamaConnectionError: If unable to connect to Ollama
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()["response"]
        except httpx.ConnectError:
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running with 'ollama serve'"
            )
        except httpx.HTTPStatusError as e:
            raise OllamaConnectionError(f"Ollama HTTP error: {e}")
        except Exception as e:
            raise OllamaConnectionError(f"Unexpected error: {e}")
    
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Generate text using Ollama with streaming.
        
        This method yields text chunks as they are generated,
        allowing for real-time display of the response.
        
        Args:
            prompt: The text prompt to send to the LLM
            system: Optional system prompt to set behavior
            temperature: Controls randomness
        
        Yields:
            str: Text chunks as they are generated
        
        Raises:
            OllamaConnectionError: If unable to connect to Ollama
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue
        except httpx.ConnectError:
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self.base_url}"
            )
        except httpx.HTTPStatusError as e:
            raise OllamaConnectionError(f"Ollama HTTP error: {e}")
    
    async def embed(self, text: str) -> List[float]:
        """
        Generate embeddings for the given text.
        
        Args:
            text: Text to generate embeddings for
        
        Returns:
            List[float]: Embedding vector
        
        Raises:
            OllamaConnectionError: If unable to connect to Ollama
        """
        url = f"{self.base_url}/api/embeddings"
        
        payload = {
            "model": self.embed_model,
            "prompt": text
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()["embedding"]
        except httpx.ConnectError:
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self.base_url}"
            )
        except httpx.HTTPStatusError as e:
            raise OllamaConnectionError(f"Ollama HTTP error: {e}")
    
    async def health_check(self) -> bool:
        """
        Check if Ollama is reachable and responding.
        
        Returns:
            bool: True if Ollama is healthy, False otherwise
        """
        url = f"{self.base_url}/api/version"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return True
        except Exception:
            return False
