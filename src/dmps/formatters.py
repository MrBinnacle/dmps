"""
Output formatters for conversational and structured modes.
"""

import json
from typing import Any, Dict, Final

from .profiler import performance_monitor
from .schema import OptimizationRequest, OptimizedResult


class ConversationalFormatter:
    """Formats output in conversational style with performance optimization"""

    # Pre-compiled format templates for performance
    _IMPROVEMENT_TEMPLATE: Final = (
        "I've optimized your prompt with the following improvements:"
    )
    _SUGGESTION_TEMPLATE: Final = "**Suggestions for further improvement:**"
    _PROMPT_HEADER: Final = "**Optimized Prompt:**"

    @performance_monitor(threshold=0.02)
    def format(
        self,
        optimization_data: Dict[str, Any],
        request: OptimizationRequest,
        optimized_prompt: str,
    ) -> OptimizedResult:
        """Format optimization result conversationally with performance monitoring"""

        # Build conversational explanation efficiently
        explanation_sections = []

        # Add improvements section if present
        applied_improvements = optimization_data.get("improvements")
        if applied_improvements:
            improvement_lines = [self._IMPROVEMENT_TEMPLATE]
            improvement_lines.extend(
                f"• {improvement}" for improvement in applied_improvements
            )
            improvement_lines.append("")
            explanation_sections.extend(improvement_lines)

        # Add optimized prompt section
        explanation_sections.extend([self._PROMPT_HEADER, optimized_prompt])

        # Add suggestions section if present
        if request.missing_info:
            suggestion_lines = ["", self._SUGGESTION_TEMPLATE]
            suggestion_lines.extend(
                f"• {suggestion}" for suggestion in request.missing_info
            )
            explanation_sections.extend(suggestion_lines)

        formatted_output = "\n".join(explanation_sections)

        return OptimizedResult(
            optimized_prompt=formatted_output,
            improvements=optimization_data.get("improvements", []),
            methodology_applied="4-D Conversational",
            metadata={
                "original_length": len(request.raw_input),
                "optimized_length": len(optimized_prompt),
                "intent": request.intent,
                "platform": request.platform,
                "techniques_used": optimization_data.get("techniques_applied", []),
            },
            format_type="conversational",
        )


class StructuredFormatter:
    """Formats output in structured JSON style with performance optimization"""

    # Pre-defined structure template for performance
    _BASE_STRUCTURE: Final = {
        "optimization_result": {"methodology": "4-D Optimization", "version": "1.0"}
    }

    @performance_monitor(threshold=0.02)
    def format(
        self,
        optimization_data: Dict[str, Any],
        request: OptimizationRequest,
        optimized_prompt: str,
    ) -> OptimizedResult:
        """Format optimization result as structured data with performance monitoring"""

        # Build structured output efficiently
        original_words = request.raw_input.split()
        optimized_words = optimized_prompt.split()

        structured_output = {
            "optimization_result": {
                "original_prompt": request.raw_input,
                "optimized_prompt": optimized_prompt,
                "intent_detected": request.intent,
                "target_platform": request.platform,
                "improvements_applied": optimization_data.get("improvements", []),
                "techniques_used": optimization_data.get("techniques_applied", []),
                "analysis": {
                    "original_length": len(request.raw_input),
                    "optimized_length": len(optimized_prompt),
                    "word_count_original": len(original_words),
                    "word_count_optimized": len(optimized_words),
                    "constraints_identified": request.constraints,
                    "missing_information": request.missing_info,
                },
                "metadata": {
                    **self._BASE_STRUCTURE["optimization_result"],
                    "components_analyzed": optimization_data.get("components", {}),
                },
            }
        }

        # Optimize JSON serialization
        formatted_json = json.dumps(
            structured_output, indent=2, ensure_ascii=False, separators=(",", ": ")
        )

        return OptimizedResult(
            optimized_prompt=formatted_json,
            improvements=optimization_data.get("improvements", []),
            methodology_applied="4-D Structured",
            metadata=structured_output["optimization_result"]["metadata"],
            format_type="structured",
        )
