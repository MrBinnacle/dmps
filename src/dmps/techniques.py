"""
Optimization techniques for prompt enhancement.
"""

from typing import List, Dict, Any
from .schema import OptimizationRequest


class OptimizationTechniques:
    """Collection of optimization techniques"""
    
    ROLE_ASSIGNMENTS = {
        "creative": "You are an expert creative writer and storyteller with years of experience crafting engaging narratives",
        "technical": "You are a senior software engineer and technical architect with deep expertise in best practices",
        "educational": "You are an experienced educator and learning specialist skilled at explaining complex concepts",
        "complex": "You are a strategic analyst and systems thinking expert with strong analytical capabilities",
        "general": "You are a helpful AI assistant with expertise across multiple domains"
    }
    
    TECHNIQUE_MAPPINGS = {
        "creative": ["role_assignment", "tone_emphasis", "structure_guidance", "creative_constraints"],
        "technical": ["role_assignment", "precision_focus", "step_by_step", "constraint_based"],
        "educational": ["role_assignment", "clear_structure", "examples_included", "scaffolding"],
        "complex": ["role_assignment", "systematic_framework", "chain_of_thought", "decomposition"],
        "general": ["role_assignment", "clear_structure", "context_enhancement"]
    }
    
    @classmethod
    def generate_role(cls, intent: str) -> str:
        """Generate appropriate role assignment"""
        return cls.ROLE_ASSIGNMENTS.get(intent, cls.ROLE_ASSIGNMENTS["general"])
    
    @classmethod
    def enhance_context(cls, request: OptimizationRequest) -> str:
        """Add missing context based on identified gaps"""
        context_additions = []
        
        for gap in request.missing_info:
            if gap == "audience":
                context_additions.append("Please specify your target audience and their expertise level.")
            elif gap == "output_format":
                context_additions.append("Please specify the desired output format (e.g., list, paragraph, structured data).")
            elif gap == "constraints":
                context_additions.append("Consider any length, style, or other constraints for the output.")
            elif gap == "technical_context":
                context_additions.append("Please specify the programming language, framework, or technical environment.")
            elif gap == "creative_context":
                context_additions.append("Please specify the desired tone, style, genre, or creative direction.")
            elif gap == "educational_context":
                context_additions.append("Please specify the learning level and background knowledge assumed.")
        
        return "\n".join(context_additions) if context_additions else ""
    
    @classmethod
    def build_structure_guidance(cls, intent: str) -> str:
        """Build structure guidance based on intent"""
        structures = {
            "creative": "Structure your response with: 1) Setting/Context, 2) Character Development, 3) Plot Progression, 4) Resolution/Conclusion",
            "technical": "Structure your response with: 1) Problem Analysis, 2) Solution Approach, 3) Implementation Details, 4) Testing/Validation",
            "educational": "Structure your response with: 1) Learning Objectives, 2) Core Concepts, 3) Examples/Applications, 4) Summary/Review",
            "complex": "Structure your response with: 1) Problem Decomposition, 2) Analysis Framework, 3) Key Insights, 4) Recommendations",
            "general": "Structure your response with clear sections and logical flow"
        }
        
        return structures.get(intent, structures["general"])
    
    @classmethod
    def format_constraints(cls, constraints: List[str]) -> str:
        """Format constraints into clear instructions"""
        if not constraints:
            return ""
        
        formatted = "Please adhere to these constraints:\n"
        for constraint in constraints:
            formatted += f"- {constraint}\n"
        
        return formatted.strip()
    
    @classmethod
    def get_techniques_for_intent(cls, intent: str) -> List[str]:
        """Get applicable techniques for a given intent"""
        return cls.TECHNIQUE_MAPPINGS.get(intent, cls.TECHNIQUE_MAPPINGS["general"])
    
    @classmethod
    def apply_technique(cls, technique: str, request: OptimizationRequest) -> str:
        """Apply a specific optimization technique"""
        if technique == "role_assignment":
            return cls.generate_role(request.intent)
        elif technique == "context_enhancement":
            return cls.enhance_context(request)
        elif technique == "structure_guidance":
            return cls.build_structure_guidance(request.intent)
        elif technique == "constraint_based":
            return cls.format_constraints(request.constraints)
        elif technique == "chain_of_thought":
            return "Think through this step-by-step, showing your reasoning process."
        elif technique == "examples_included":
            return "Include relevant examples to illustrate your points."
        elif technique == "precision_focus":
            return "Be specific and precise in your response, avoiding vague generalizations."
        else:
            return ""
