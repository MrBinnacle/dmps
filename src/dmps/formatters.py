"""
Output formatters for conversational and structured modes.
"""

import json
from typing import Dict, Any
from .schema import OptimizedResult, OptimizationRequest


class ConversationalFormatter:
    """Formats output in conversational style"""
    
    def format(self, optimization_data: Dict[str, Any], 
               request: OptimizationRequest, 
               optimized_prompt: str) -> OptimizedResult:
        """Format optimization result conversationally"""
        
        # Create conversational explanation
        explanation_parts = []
        
        if optimization_data.get("improvements"):
            explanation_parts.append("I've optimized your prompt with the following improvements:")
            for improvement in optimization_data["improvements"]:
                explanation_parts.append(f"• {improvement}")
            explanation_parts.append("")
        
        explanation_parts.append("**Optimized Prompt:**")
        explanation_parts.append(optimized_prompt)
        
        if request.missing_info:
            explanation_parts.append("")
            explanation_parts.append("**Suggestions for further improvement:**")
            for suggestion in request.missing_info:
                explanation_parts.append(f"• {suggestion}")
        
        formatted_output = "\n".join(explanation_parts)
        
        return OptimizedResult(
            optimized_prompt=formatted_output,
            improvements=optimization_data.get("improvements", []),
            methodology_applied="4-D Conversational",
            metadata={
                "original_length": len(request.raw_input),
                "optimized_length": len(optimized_prompt),
                "intent": request.intent,
                "platform": request.platform,
                "techniques_used": optimization_data.get("techniques_applied", [])
            },
            format_type="conversational"
        )


class StructuredFormatter:
    """Formats output in structured JSON style"""
    
    def format(self, optimization_data: Dict[str, Any], 
               request: OptimizationRequest, 
               optimized_prompt: str) -> OptimizedResult:
        """Format optimization result as structured data"""
        
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
                    "word_count_original": len(request.raw_input.split()),
                    "word_count_optimized": len(optimized_prompt.split()),
                    "constraints_identified": request.constraints,
                    "missing_information": request.missing_info
                },
                "metadata": {
                    "methodology": "4-D Optimization",
                    "version": "1.0",
                    "components_analyzed": optimization_data.get("components", {})
                }
            }
        }
        
        formatted_json = json.dumps(structured_output, indent=2, ensure_ascii=False)
        
        return OptimizedResult(
            optimized_prompt=formatted_json,
            improvements=optimization_data.get("improvements", []),
            methodology_applied="4-D Structured",
            metadata=structured_output["optimization_result"]["metadata"],
            format_type="structured"
        )