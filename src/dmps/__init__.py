"""
DMPS - Dual-Mode Prompt System for AI prompt optimization using 4-D methodology.

The DMPS system helps optimize AI prompts by:
1. DECONSTRUCTING the input to understand intent and identify gaps
2. DEVELOPING optimization strategies based on detected patterns
3. DESIGNING structured improvements using proven techniques
4. DELIVERING formatted output in conversational or structured modes
"""

from .optimizer import PromptOptimizer
from .engine import OptimizationEngine
from .schema import OptimizationRequest, OptimizedResult, ValidationResult
from .intent import IntentClassifier, GapAnalyzer
from .techniques import OptimizationTechniques
from .formatters import ConversationalFormatter, StructuredFormatter
from .validation import InputValidator

__version__ = '0.1.0'
__author__ = 'MrBinnacle'
__email__ = 'your.email@example.com'
__description__ = 'Dual-Mode Prompt System for AI prompt optimization'

# Main API
__all__ = [
    'PromptOptimizer',
    'OptimizationEngine', 
    'OptimizationRequest',
    'OptimizedResult',
    'ValidationResult',
    'IntentClassifier',
    'GapAnalyzer',
    'OptimizationTechniques',
    'ConversationalFormatter',
    'StructuredFormatter',
    'InputValidator'
]

# Convenience function for quick optimization
def optimize_prompt(prompt: str, mode: str = "conversational", platform: str = "claude"):
    """Quick optimization function for simple use cases"""
    optimizer = PromptOptimizer()
    result, validation = optimizer.optimize(prompt, mode, platform)
    return result.optimized_prompt
