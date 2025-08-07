"""
LLM API client for routing requests to different providers
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional, Any, Callable
import time

if TYPE_CHECKING:
    from langchain.chat_models import ChatOpenAI, ChatAnthropic

try:
    from langchain.chat_models import ChatOpenAI, ChatAnthropic

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    ChatOpenAI = None
    ChatAnthropic = None


@dataclass
class LLMResponse:
    """Response from LLM API"""

    content: str
    model: str
    tokens_used: int
    cost_estimate: float
    response_time: float


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response from LLM"""
        pass


class MockLLMClient(LLMClient):
    """Mock LLM client for testing and fallback"""

    def __init__(self, model_name: str = "mock-model"):
        self.model_name = model_name

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate mock response"""
        start_time = time.time()

        # Simple mock optimization based on prompt analysis
        optimized = self._mock_optimize(prompt)

        response_time = time.time() - start_time
        tokens = len(optimized.split()) * 1.3  # Rough token estimate

        return LLMResponse(
            content=optimized,
            model=self.model_name,
            tokens_used=int(tokens),
            cost_estimate=tokens * 0.0001,  # Mock cost
            response_time=response_time,
        )

    def _mock_optimize(self, prompt: str) -> str:
        """Mock optimization logic"""
        if len(prompt) < 10:
            return f"Please provide more context for: {prompt}"

        # Add role and structure
        optimized = f"You are an expert assistant. {prompt}"

        # Add constraints if missing
        if "word" not in prompt.lower() and "length" not in prompt.lower():
            optimized += " Please provide a comprehensive response."

        return optimized


class BaseLangChainClient(LLMClient):
    """Base class for LangChain-powered clients"""

    def __init__(
        self,
        api_key: Optional[str],
        env_key: str,
        model: str,
        cost_per_token: float,
    ) -> None:
        self.api_key = api_key or os.getenv(env_key)
        self.model = model
        self.cost_per_token = cost_per_token
        self._client: Optional[Callable[[list], Any]] = None

    def _create_client(self) -> Callable[[list], Any]:
        """Override in subclasses to create specific client"""
        raise NotImplementedError

    @property
    def client(self) -> Optional[Callable[[list], Any]]:
        """Lazy-load LangChain client"""
        if self._client is None and LANGCHAIN_AVAILABLE and self.api_key:
            self._client = self._create_client()
        return self._client

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using LangChain"""
        start_time = time.time()

        client = self.client
        if client is not None:
            try:
                # Import within guarded scope to satisfy type checkers
                from langchain.schema import (  # type: ignore[reportMissingImports]
                    HumanMessage as _HumanMessage,
                )

                message = _HumanMessage(content=prompt)
                response = client([message])
                content = response.content

                tokens = len(content.split()) * 1.3

                return LLMResponse(
                    content=content,
                    model=self.model,
                    tokens_used=int(tokens),
                    cost_estimate=tokens * self.cost_per_token,
                    response_time=time.time() - start_time,
                )
            except Exception:
                pass

        return MockLLMClient(f"{self.model}-fallback").generate(prompt, **kwargs)


class OpenAIClient(BaseLangChainClient):
    """OpenAI API client"""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"
    ) -> None:
        super().__init__(api_key, "OPENAI_API_KEY", model, 0.002)

    def _create_client(self) -> Callable[[list], Any]:
        return ChatOpenAI(
            openai_api_key=self.api_key,
            model_name=self.model,
            temperature=0.7,
        )


class AnthropicClient(BaseLangChainClient):
    """Anthropic Claude API client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-sonnet-20240229",
    ) -> None:
        super().__init__(api_key, "ANTHROPIC_API_KEY", model, 0.015)

    def _create_client(self) -> Callable[[list], Any]:
        return ChatAnthropic(
            anthropic_api_key=self.api_key,
            model=self.model,
            temperature=0.7,
        )


class LLMRouter:
    """Routes requests to appropriate LLM clients with lazy initialization"""

    PLATFORM_MAPPING = {
        "chatgpt": "openai",
        "claude": "anthropic",
        "huggingface": "huggingface_api",
        "local": "huggingface_local",
        "generic": "mock",
        "gemini": "mock",
    }

    def __init__(self):
        self._clients: Dict[str, Optional[LLMClient]] = {}

    def _get_or_create_client(self, client_key: str) -> LLMClient:
        """Lazy-load clients on first use"""
        if client_key not in self._clients:
            if client_key == "openai":
                self._clients[client_key] = OpenAIClient()
            elif client_key == "anthropic":
                self._clients[client_key] = AnthropicClient()
            elif client_key == "huggingface_local":
                from .huggingface_client import HuggingFaceLocalClient

                self._clients[client_key] = HuggingFaceLocalClient()
            elif client_key == "huggingface_api":
                from .huggingface_client import HuggingFaceAPIClient

                self._clients[client_key] = HuggingFaceAPIClient()
            else:
                self._clients[client_key] = MockLLMClient()

        return self._clients[client_key]

    def generate(self, prompt: str, platform: str = "chatgpt", **kwargs) -> LLMResponse:
        """Generate response using specified platform"""
        client_key = self.PLATFORM_MAPPING.get(platform, "mock")
        client = self._get_or_create_client(client_key)
        return client.generate(prompt, **kwargs)


# Global router instance
llm_router = LLMRouter()
