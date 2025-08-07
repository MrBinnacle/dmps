"""
Centralized configuration management
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """LLM API configuration"""

    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None

    def __post_init__(self):
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = self.anthropic_api_key or os.getenv(
            "ANTHROPIC_API_KEY"
        )
        self.huggingface_api_key = self.huggingface_api_key or os.getenv(
            "HUGGINGFACE_API_KEY"
        )


@dataclass
class SecurityConfig:
    """Security configuration"""

    max_file_size: int = 10 * 1024 * 1024  # 10MB
    max_lines: int = 1000
    allowed_extensions: tuple = (".txt", ".md", ".json", ".yaml", ".yml")


# Global config instances

llm_config = LLMConfig()
security_config = SecurityConfig()
