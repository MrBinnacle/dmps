"""
Hugging Face integration for DMPS
"""

import os
import time
from typing import Optional

from .llm_client import LLMClient, LLMResponse, MockLLMClient

try:
    from transformers import pipeline as hf_pipeline  # type: ignore

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    hf_pipeline = None

try:
    import requests  # type: ignore[reportMissingImports]

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None


class BaseHuggingFaceClient(LLMClient):
    """Base class for Hugging Face clients"""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def _process_output(self, content: str, prompt: str) -> str:
        """Clean and process model output"""
        prefix = f"Optimize this prompt: {prompt}"
        return content.replace(prefix, "").strip() or f"Optimized: {prompt}"

    def _create_response(
        self,
        content: str,
        start_time: float,
        cost: float = 0.0,
    ) -> LLMResponse:
        """Create standardized response"""
        return LLMResponse(
            content=content,
            model=self.model_name,
            tokens_used=len(content.split()),
            cost_estimate=cost,
            response_time=time.time() - start_time,
        )


class HuggingFaceLocalClient(BaseHuggingFaceClient):
    """Local Hugging Face model client"""

    def __init__(self, model_name: str = "microsoft/DialoGPT-medium") -> None:
        super().__init__(model_name)
        self._pipeline = None

    @property
    def pipeline(self):
        """Lazy-load transformers pipeline"""
        if self._pipeline is None and TRANSFORMERS_AVAILABLE:
            try:
                from transformers import pipeline

                self._pipeline = pipeline("text-generation", model=self.model_name)
            except Exception:
                pass
        return self._pipeline

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate using local model"""
        start_time = time.time()

        pipe = self.pipeline
        if pipe is not None:
            try:
                outputs = pipe(
                    f"Optimize this prompt: {prompt}",
                    max_length=150,
                    num_return_sequences=1,
                    temperature=0.7,
                )
                content = self._process_output(outputs[0]["generated_text"], prompt)
                return self._create_response(content, start_time)
            except Exception:
                pass

        return MockLLMClient(f"{self.model_name}-fallback").generate(prompt, **kwargs)


class HuggingFaceAPIClient(BaseHuggingFaceClient):
    """Hugging Face Inference API client"""

    def __init__(
        self,
        model_name: str = "microsoft/DialoGPT-large",
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(model_name)
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate using API"""
        start_time = time.time()

        if REQUESTS_AVAILABLE and self.api_key:
            try:
                import requests

                response = requests.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"inputs": f"Optimize this prompt: {prompt}"},
                    timeout=30,
                )

                if response.status_code == 200:
                    result = response.json()
                    raw_content = result[0]["generated_text"] if result else prompt
                    content = self._process_output(raw_content, prompt)
                    cost = 0.0001 * len(content.split())
                    return self._create_response(content, start_time, cost)
            except Exception:
                pass

        return MockLLMClient(f"{self.model_name}-fallback").generate(prompt, **kwargs)
