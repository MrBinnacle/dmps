"""
Core optimization engine implementing the 4-D methodology.
"""

import re
from typing import List, Optional, Dict, Any
from .schema import OptimizationRequest
from .intent import IntentClassifier, GapAnalyzer
from .techniques import OptimizationTechniques


class OptimizationEngine:
    """Core 4-D optimization engine"""
    
    def extract_intent(self, prompt_input: str) -> OptimizationRequest:
        """DECONSTRUCT: Extract intent and identify gaps"""
        intent = IntentClassifier.detect_intent(prompt_input)
        missing_info = GapAnalyzer.identify_gaps(prompt_input, intent)
        constraints = self._extract_constraints(prompt_input)
        
        return OptimizationRequest(
            raw_input=prompt_input,
            intent=intent,
            output_type=self._infer_output_type(prompt_input, intent),
            platform="claude",  # Default platform
            constraints=constraints,
            missing_info=missing_info
        )
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract explicit constraints from text"""
        constraints = []
        text_lower = text.lower()
        
        # Length constraints
        length_patterns = [
            r"(\d+)\s*words?",
            r"(\d+)\s*characters?",
            r"(\d+)\s*pages?",
            r"under (\d+)",
            r"less than (\d+)",
            r"maximum (\d+)"
        ]
        for pattern in length_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                constraints.append(f"Length limit: {matches[0]} words/characters")
        
        # Style constraints
        style_keywords = ["formal", "informal", "professional", "casual", "academic", "conversational"]
        for keyword in style_keywords:
            if keyword in text_lower:
                constraints.append(f"Style: {keyword}")
        
        # Language constraints
        if "python" in text_lower:
            constraints.append("Language: Python")
        elif "javascript" in text_lower:
            constraints.append("Language: JavaScript")
        elif "java" in text_lower and "javascript" not in text_lower:
            constraints.append("Language: Java")
        
        return constraints
    
    def _infer_output_type(self, text: str, intent: str) -> str:
        """Infer desired output type"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["list", "bullet", "numbered"]):
            return "list"
        elif any(word in text_lower for word in ["json", "structured", "data"]):
            return "structured"
        elif any(word in text_lower for word in ["table", "chart", "grid"]):
            return "table"
        elif intent == "creative":
            return "narrative"
        elif intent == "technical":
            return "code"
        else:
            return "text"
    
    def apply_optimization(self, request: OptimizationRequest) -> Dict[str, Any]:
        """DEVELOP: Apply optimization techniques"""
        techniques = OptimizationTechniques.get_techniques_for_intent(request.intent)
        applied_techniques = []
        optimizations = {}
        
        for technique in techniques:
            result = OptimizationTechniques.apply_technique(technique, request)
            if result:
                optimizations[technique] = result
                applied_techniques.append(technique)
        
        return {
            "techniques_applied": applied_techniques,
            "optimizations": optimizations,
            "role": OptimizationTechniques.generate_role(request.intent),
            "structure_guidance": OptimizationTechniques.build_structure_guidance(request.intent),
            "context_enhancements": OptimizationTechniques.enhance_context(request),
            "formatted_constraints": OptimizationTechniques.format_constraints(request.constraints)
        }
    
    def assemble_prompt(self, optimization_data: Dict[str, Any], request: OptimizationRequest) -> str:
        """DELIVER: Assemble final optimized prompt"""
        components = []
        
        # Add role assignment
        if "role" in optimization_data and optimization_data["role"]:
            components.append(optimization_data["role"])
        
        # Add the original request with enhancements
        enhanced_request = request.raw_input
        
        # Add context enhancements if any gaps were identified
        if optimization_data.get("context_enhancements"):
            components.append(f"Context: {optimization_data['context_enhancements']}")
        
        # Add structure guidance
        if optimization_data.get("structure_guidance"):
            components.append(f"Structure: {optimization_data['structure_guidance']}")
        
        # Add constraints
        if optimization_data.get("formatted_constraints"):
            components.append(optimization_data["formatted_constraints"])
        
        # Add the main request
        components.append(f"Task: {enhanced_request}")
        
        # Add platform-specific optimizations
        if request.platform == "chatgpt":
            components.append("Please provide a comprehensive and well-structured response.")
        elif request.platform == "claude":
            components.append("Please think carefully and provide a thoughtful, detailed response.")
        
        return "\n\n".join(filter(None, components))
    
    def optimize_prompt(self, prompt_input: str, platform: str = "claude") -> tuple:
        """Complete optimization pipeline"""
        # Extract intent and create request
        request = self.extract_intent(prompt_input)
        request.platform = platform
        
        # Apply optimizations
        optimization_data = self.apply_optimization(request)
        
        # Assemble final prompt
        optimized_prompt = self.assemble_prompt(optimization_data, request)
        
        return optimized_prompt, optimization_data, request
