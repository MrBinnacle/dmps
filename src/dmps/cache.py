"""
Performance optimization with caching and lazy loading.
"""

from functools import lru_cache
from typing import Final


class PerformanceCache:
    """Caching layer for expensive operations"""

    # Cache sizes optimized for memory usage
    INTENT_CACHE_SIZE: Final = 128
    VALIDATION_CACHE_SIZE: Final = 256

    @staticmethod
    @lru_cache(maxsize=INTENT_CACHE_SIZE)
    def cached_intent_classification(prompt_hash: str, prompt: str) -> str:
        """Cache intent classification results"""
        from .intent import IntentClassifier

        classifier = IntentClassifier()
        return classifier.classify(prompt)

    @staticmethod
    @lru_cache(maxsize=VALIDATION_CACHE_SIZE)
    def cached_path_validation(filepath: str) -> bool:
        """Cache path validation results"""
        from .security import SecurityConfig

        return SecurityConfig.is_safe_path(filepath)

    @staticmethod
    def get_prompt_hash(prompt: str) -> str:
        """Generate hash for prompt caching"""
        return str(hash(prompt.strip().lower()))


# Lazy-loaded singletons for expensive objects
_intent_classifier = None
_optimization_engine = None


def get_intent_classifier():
    """Lazy-loaded intent classifier singleton"""
    global _intent_classifier
    if _intent_classifier is None:
        from .intent import IntentClassifier

        _intent_classifier = IntentClassifier()
    return _intent_classifier


def get_optimization_engine():
    """Lazy-loaded optimization engine singleton"""
    global _optimization_engine
    if _optimization_engine is None:
        from .engine import OptimizationEngine

        _optimization_engine = OptimizationEngine()
    return _optimization_engine
