"""
DMPS - Dual-Mode Prompt System for AI prompt optimization using 4-D methodology.

Naming Conventions:
- Classes: PascalCase (e.g., PromptOptimizer)
- Functions/Methods: snake_case (e.g., optimize_prompt)
- Variables: descriptive_snake_case (e.g., user_prompt, detected_intent)
- Constants: UPPER_SNAKE_CASE (e.g., MAX_INPUT_LENGTH)
- Private methods: _snake_case (e.g., _validate_input)

The DMPS system helps optimize AI prompts by:
1. DECONSTRUCTING the input to understand intent and identify gaps
2. DEVELOPING optimization strategies based on detected patterns
3. DESIGNING structured improvements using proven techniques
4. DELIVERING formatted output in conversational or structured modes
"""

from .engine import OptimizationEngine
from .formatters import ConversationalFormatter, StructuredFormatter
from .intent import IntentClassifier
from .optimizer import PromptOptimizer
from .repl import DMPSShell
from .schema import OptimizationRequest, OptimizedResult, ValidationResult
from .techniques import OptimizationTechniques
from .validation import InputValidator

__version__ = "0.2.1"
__author__ = "MrBinnacle"
__email__ = "your.email@example.com"
__description__ = "Dual-Mode Prompt System for AI prompt optimization"

# Main API
__all__ = [
    "PromptOptimizer",
    "OptimizationEngine",
    "OptimizationRequest",
    "OptimizedResult",
    "ValidationResult",
    "IntentClassifier",
    "OptimizationTechniques",
    "ConversationalFormatter",
    "StructuredFormatter",
    "InputValidator",
    "DMPSShell",
]

# Convenience function for quick optimization


def optimize_prompt(
    user_prompt: str,
    output_mode: str = "conversational",
    target_platform: str = "claude",
):
    """Quick optimization function following naming conventions

    Args:
        user_prompt: The input prompt to optimize
        output_mode: Format mode (conversational/structured)
        target_platform: AI platform (claude/chatgpt/gemini/generic)

    Returns:
        Optimized prompt string
    """
    prompt_optimizer = PromptOptimizer()
    optimization_result, validation_result = prompt_optimizer.optimize(
        user_prompt, output_mode, target_platform
    )
    return optimization_result.optimized_prompt
