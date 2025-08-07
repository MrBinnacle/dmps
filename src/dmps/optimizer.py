"""
Main orchestrator for prompt optimization.
"""

import json
import uuid
from typing import Final, Literal, Tuple

from .evaluation import context_evaluator
from .formatters import ConversationalFormatter, StructuredFormatter
from .schema import OptimizedResult, ValidationResult
from .token_tracker import token_tracker
from .validation import InputValidator


class PromptOptimizer:
    """Main orchestrator for prompt optimization"""

    # Pre-instantiated formatters for performance
    _FORMATTERS: Final = {
        "conversational": ConversationalFormatter(),
        "structured": StructuredFormatter(),
    }

    def __init__(self):
        # Lazy-load expensive components for better startup performance
        self._engine = None
        self._validator = None

    @property
    def engine(self):
        """Lazy-loaded optimization engine"""
        if self._engine is None:
            from .cache import get_optimization_engine

            self._engine = get_optimization_engine()
        return self._engine

    @property
    def validator(self):
        """Lazy-loaded input validator"""
        if self._validator is None:
            self._validator = InputValidator()
        return self._validator

    def optimize(
        self, prompt_input: str, mode: str = "conversational", platform: str = "claude"
    ) -> Tuple[OptimizedResult, ValidationResult]:
        """Main optimization entry point with token tracking and evaluation"""

        # Start token tracking
        operation_id = str(uuid.uuid4())[:8]
        trace_context = token_tracker.start_trace(operation_id, prompt_input)

        validation = self.validator.validate_input(prompt_input, mode)
        if not validation.is_valid:
            return self._create_error_result(validation.errors, mode), validation

        try:
            sanitized_input = validation.sanitized_input or ""
            # Use cached intent classification for performance
            from .cache import PerformanceCache

            prompt_hash = PerformanceCache.get_prompt_hash(sanitized_input)
            cached_intent = PerformanceCache.cached_intent_classification(
                prompt_hash, sanitized_input
            )

            request = self.engine.extract_intent(sanitized_input)
            request.intent = cached_intent  # Use cached result
            request.platform = platform

            optimization_data = self.engine.apply_optimization(request)
            optimized_prompt = self.engine.assemble_prompt(optimization_data, request)

            formatter = self._FORMATTERS[mode]
            result = formatter.format(optimization_data, request, optimized_prompt)

            # Complete token tracking
            techniques_applied = optimization_data.get("techniques_applied", [])
            trace = token_tracker.complete_trace(
                trace_context, optimized_prompt, techniques_applied, platform
            )

            # Evaluate context engineering effectiveness
            evaluation = context_evaluator.evaluate(
                prompt_input,
                optimized_prompt,
                trace_context["original_tokens"],
                token_tracker.estimate_tokens(optimized_prompt),
            )

            # Add tracking metadata to result
            result.metadata.update(
                {
                    "token_metrics": {
                        "original_tokens": trace_context["original_tokens"],
                        "optimized_tokens": trace.metrics.input_tokens,
                        "token_reduction": trace.token_reduction,
                        "cost_estimate": trace.metrics.cost_estimate,
                    },
                    "evaluation": {
                        "overall_score": evaluation.overall_score,
                        "token_efficiency": evaluation.token_efficiency,
                        "degradation_detected": evaluation.degradation_detected,
                    },
                    "operation_id": operation_id,
                }
            )

            # Add evaluation warnings if degradation detected
            if evaluation.degradation_detected:
                validation.warnings.append(
                    "Quality degradation detected in optimization"
                )
                validation.warnings.extend(evaluation.recommendations)

            return result, validation

        except (ValueError, TypeError, AttributeError) as e:
            # Handle known processing errors with secure sanitization
            from .error_handler import error_handler

            try:
                sanitized_msg = error_handler.sanitize_error_message(str(e))
            except Exception:
                sanitized_msg = "Processing error occurred"

            return self._create_fallback_result(
                validation.sanitized_input or "", sanitized_msg, mode
            ), ValidationResult(
                is_valid=False,
                errors=[f"Optimization failed: {sanitized_msg}"],
                warnings=["Using emergency fallback"],
                sanitized_input=validation.sanitized_input,
            )
        except ImportError as e:
            # Handle missing dependencies with proper logging
            from .error_handler import error_handler

            error_handler.handle_error(e, "missing_dependency")
            return self._create_fallback_result(
                validation.sanitized_input or "", "Missing dependency", mode
            ), ValidationResult(
                is_valid=False,
                errors=["Required component unavailable"],
                warnings=["Using emergency fallback"],
                sanitized_input=validation.sanitized_input,
            )
        except Exception as e:
            # Handle all unexpected errors with maximum security
            from .error_handler import error_handler

            try:
                # Log for security monitoring but don't expose details
                error_handler.handle_error(e, "optimization_unexpected")
                # Always return generic message for unknown errors
                safe_msg = "Internal processing error"
            except Exception:
                # Fallback if error handler itself fails
                safe_msg = "System error occurred"

            return self._create_fallback_result(
                validation.sanitized_input or "", safe_msg, mode
            ), ValidationResult(
                is_valid=False,
                errors=["Internal processing error occurred"],
                warnings=["Using emergency fallback"],
                sanitized_input=validation.sanitized_input,
            )

    def _create_error_result(self, errors: list, mode: str) -> OptimizedResult:
        """Create error result for validation failures"""
        error_message = "Optimization failed:\n" + "\n".join(
            f"• {error}" for error in errors
        )

        error_prompt = (
            json.dumps(
                {"error": True, "message": error_message, "errors": errors}, indent=2
            )
            if mode == "structured"
            else (f"**Error:**\n{error_message}")
        )

        format_type: Literal["conversational", "structured"] = (
            "structured" if mode == "structured" else "conversational"
        )

        return OptimizedResult(
            optimized_prompt=error_prompt,
            improvements=[],
            methodology_applied="Error Handling",
            metadata={"error": True, "error_count": len(errors)},
            format_type=format_type,
        )

    def _create_fallback_result(
        self, input_text: str, error: str, mode: str
    ) -> OptimizedResult:
        """Create fallback result for processing failures"""
        # Sanitize error message to prevent information disclosure
        try:
            safe_error = (
                "Processing error occurred"
                if error and len(error) > 0
                else "Unknown error"
            )
        except (TypeError, AttributeError):
            safe_error = "Unknown error"

        fallback_prompt = (
            json.dumps(
                {
                    "status": "fallback",
                    "original_prompt": input_text,
                    "error": safe_error,
                },
                indent=2,
            )
            if mode == "structured"
            else (f"**Fallback:**\n{input_text}\n\nError: {safe_error}")
        )

        format_type: Literal["conversational", "structured"] = (
            "structured" if mode == "structured" else "conversational"
        )

        return OptimizedResult(
            optimized_prompt=fallback_prompt,
            improvements=["Emergency fallback applied"],
            methodology_applied="Fallback Mode",
            metadata={"fallback": True, "error": error},
            format_type=format_type,
        )
