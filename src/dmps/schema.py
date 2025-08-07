"""
Core data structures for the Dual-Mode Prompt System (DMPS).
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional


@dataclass
class OptimizationRequest:
    """Core request structure for optimization"""

    raw_input: str
    intent: str
    output_type: str
    platform: str
    constraints: List[str]
    missing_info: List[str]


@dataclass
class OptimizedResult:
    """Result structure for optimized prompts"""

    optimized_prompt: str
    improvements: List[str]
    methodology_applied: str
    metadata: Dict[str, Any]
    format_type: Literal["conversational", "structured"]


@dataclass
class ValidationResult:
    """Validation result structure"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_input: Optional[str] = None
