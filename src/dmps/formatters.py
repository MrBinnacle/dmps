"""
Output formatters for different presentation modes.
"""

import json
from typing import List, Dict, Any
from .schema import OptimizationRequest, OptimizedResult


class ConversationalFormatter:
    """Formats output for human-readable conversational mode"""
    
    @classmethod
    def format(cls, optimization_data: Dict[str, Any], request: OptimizationRequest, optimized_prompt: str) -> OptimizedResult:
        """Format for conversational output"""
        improvements = cls._generate_improvements_list(
            optimization_data["techniques_applied"], 
            request.missing_info
        )
        
        formatted_output = f"""**Your Optimized Prompt:**

{optimized_prompt}

**What Changed:**
{cls._format_improvements(improvements)}

**Optimization Applied:**
- Intent detected: {request.intent.title()}
- Techniques used: {', '.join(optimization_data['techniques_applied'])}
- Missing elements addressed: {', '.join(request.missing_info) if request.missing_info else 'None'}

**Platform Notes:**
This prompt is optimized for {request.platform}. For best results, copy the entire optimized prompt above."""

        return OptimizedResult(
            optimized_prompt=formatted_output,
            improvements=improvements,
            methodology_applied="4-D Conversational",
            metadata={
                "interactive": True,
                "intent": request.intent,
                "techniques_count": len(optimization_data["techniques_applied"])
            },
            format_type="conversational"
        )
    
    @classmethod
    def _generate_improvements_list(cls, techniques: List[str], missing_info: List[str]) -> List[str]:
        """Generate human-readable improvements list"""
        improvements = []
        
        technique_descriptions = {
            "role_assignment": "Added expert role to establish authority and context",
            "precision_focus": "Enhanced specificity and clarity of requirements",
            "chain_of_thought": "Added step-by-step reasoning structure",
            "clear_structure": "Organized content with logical flow and sections",
            "context_enhancement": "Provided additional context for better understanding",
            "creative_constraints": "Added creative parameters for better storytelling",
            "technical_specifics": "Included technical implementation details",
            "examples_included": "Added relevant examples for clarity",
            "scaffolding": "Provided learning support structure"
        }
        
        for technique in techniques:
            if technique in technique_descriptions:
                improvements.append(technique_descriptions[technique])
        
        # Add improvements for addressed gaps
        gap_descriptions = {
            "audience": "Clarified target audience and expertise level",
            "output_format": "Specified desired output format and structure",
            "constraints": "Added length and style constraints",
            "technical_context": "Included technical environment details",
            "creative_context": "Added creative direction and tone guidance",
            "educational_context": "Specified learning level and prerequisites"
        }
        
        for gap in missing_info:
            if gap in gap_descriptions:
                improvements.append(gap_descriptions[gap])
        
        return improvements
    
    @classmethod
    def _format_improvements(cls, improvements: List[str]) -> str:
        """Format improvements as bulleted list"""
        if not improvements:
            return "• No specific improvements needed - your prompt was already well-structured!"
        
        return "\n".join(f"• {improvement}" for improvement in improvements)


class StructuredFormatter:
    """Formats output for JSON/API structured mode"""
    
    @classmethod
    def format(cls, optimization_data: Dict[str, Any], request: OptimizationRequest, optimized_prompt: str) -> OptimizedResult:
        """Format for structured JSON output"""
        metadata = {
            "original_length": len(request.raw_input),
            "optimized_length": len(optimized_prompt),
            "intent_detected": request.intent,
            "techniques_applied": optimization_data["techniques_applied"],
            "gaps_identified": request.missing_info,
            "constraints_found": request.constraints,
            "platform_target": request.platform,
            "confidence_score": cls._calculate_confidence(optimization_data),
            "optimization_ratio": len(optimized_prompt) / len(request.raw_input) if request.raw_input else 1.0
        }
        
        structured_output = {
            "status": "success",
            "original_prompt": request.raw_input,
            "optimized_prompt": optimized_prompt,
            "analysis": {
                "intent": request.intent,
                "output_type": request.output_type,
                "missing_elements": request.missing_info,
                "constraints": request.constraints
            },
            "optimization": {
                "techniques_used": optimization_data["techniques_applied"],
                "improvements_made": len(optimization_data["techniques_applied"]),
                "methodology": "4-D Framework (Deconstruct, Develop, Design, Deliver)"
            },
            "metadata": metadata
        }
        
        return OptimizedResult(
            optimized_prompt=json.dumps(structured_output, indent=2),
            improvements=optimization_data["techniques_applied"],
            methodology_applied="4-D Structured",
            metadata=metadata,
            format_type="structured"
        )
    
    @classmethod
    def _calculate_confidence(cls, optimization_data: Dict[str, Any]) -> float:
        """Calculate optimization confidence score"""
        base_score = 0.7
        technique_bonus = len(optimization_data["techniques_applied"]) * 0.05
        
        # Cap at 0.95 to indicate there's always room for improvement
        return min(0.95, base_score + technique_bonus)
