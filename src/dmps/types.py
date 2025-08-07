"""
Centralized type definitions for optional dependencies
"""

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from transformers import Pipeline
    from requests import Response
    from langchain.schema import BaseMessage
else:
    Pipeline = Any
    Response = Any
    BaseMessage = Any


@runtime_checkable
class LLMPipeline(Protocol):
    """Protocol for HuggingFace pipeline interface"""

    def __call__(self, text: str, **kwargs) -> list[dict[str, Any]]:
        ...


@runtime_checkable
class HTTPClient(Protocol):
    """Protocol for HTTP client interface"""

    def post(self, url: str, **kwargs) -> Any:
        ...


# Type aliases for cleaner code
OptionalPipeline = Pipeline | None
OptionalHTTPClient = HTTPClient | None
