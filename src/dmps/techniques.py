"""
4-D optimization techniques implementation.
"""

import re
from typing import Dict, List


class OptimizationTechniques:
    """Implementation of 4-D optimization techniques"""
    
    def develop_clarity(self, prompt: str, intent: str) -> str:
        """Develop: Enhance clarity and specificity"""
        enhanced = prompt
        
        # Add context markers based on intent
        if intent == "technical":
            if not re.search(r"context|background|requirements", enhanced, re.IGNORECASE):
                enhanced = f"Context: {enhanced}"
        
        # Enhance vague terms
        vague_replacements = {
            r"\bsomething\b": "a specific item",
            r"\banything\b": "any relevant information",
            r"\bstuff\b": "relevant details",
            r"\bthings\b": "specific elements"
        }
        
        for pattern, replacement in vague_replacements.items():
            enhanced = re.sub(pattern, replacement, enhanced, flags=re.IGNORECASE)
        
        # Add specificity markers
        if len(enhanced.split()) < 10:
            enhanced += " Please provide detailed information."
        
        return enhanced
    
    def design_structure(self, prompt: str, platform: str, intent: str) -> str:
        """Design: Structure for target platform"""
        structured = prompt
        
        # Platform-specific optimizations
        platform_templates = {
            "claude": {
                "prefix": "Human: ",
                "structure": "Please {action}. Be thorough and accurate.",
                "suffix": ""
            },
            "chatgpt": {
                "prefix": "",
                "structure": "Act as an expert. {action}",
                "suffix": "Provide a comprehensive response."
            },
            "gemini": {
                "prefix": "",
                "structure": "{action}",
                "suffix": "Be precise and helpful."
            },
            "generic": {
                "prefix": "",
                "structure": "{action}",
                "suffix": ""
            }
        }
        
        template = platform_templates.get(platform, platform_templates["generic"])
        
        # Apply platform structure if prompt is simple
        if len(structured.split()) < 15:
            action = structured.lower().strip()
            if template["structure"] and "{action}" in template["structure"]:
                structured = template["structure"].format(action=action)
            
            if template["prefix"]:
                structured = template["prefix"] + structured
            
            if template["suffix"]:
                structured += " " + template["suffix"]
        
        # Intent-specific structuring
        if intent == "technical":
            if not structured.startswith(("Please", "Can you", "How")):
                structured = f"Please {structured.lower()}"
        
        return structured
    
    def deliver_format(self, prompt: str, output_type: str) -> str:
        """Deliver: Final formatting and validation"""
        formatted = prompt
        
        # Output type specific formatting
        format_instructions = {
            "list": "Please format your response as a numbered or bulleted list.",
            "explanation": "Please provide a clear, step-by-step explanation.",
            "code": "Please provide code examples with comments and explanations.",
            "creative": "Please be creative and engaging in your response.",
            "general": "Please provide a comprehensive and well-structured response."
        }
        
        instruction = format_instructions.get(output_type, format_instructions["general"])
        
        # Add formatting instruction if not already present
        if not re.search(r"format|structure|organize", formatted, re.IGNORECASE):
            formatted += f" {instruction}"
        
        # Ensure proper punctuation
        if not formatted.endswith(('.', '!', '?')):
            formatted += '.'
        
        # Clean up extra spaces
        formatted = re.sub(r'\s+', ' ', formatted).strip()
        
        return formatted
    
    def get_technique_description(self, technique: str) -> str:
        """Get description of optimization technique"""
        descriptions = {
            "develop_clarity": "Enhanced clarity and specificity by replacing vague terms and adding context",
            "design_structure": "Optimized structure for target platform and intent",
            "deliver_format": "Applied final formatting and output type optimization"
        }
        
        return descriptions.get(technique, "Applied optimization technique")