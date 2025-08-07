"""
Core optimization engine implementing the 4-D methodology.
"""

import re
from typing import Dict, List, Any
from .schema import OptimizationRequest
from .intent import IntentClassifier
from .techniques import OptimizationTechniques


class OptimizationEngine:
    """Core engine for prompt optimization using 4-D methodology"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.techniques = OptimizationTechniques()
    
    def extract_intent(self, prompt_input: str) -> OptimizationRequest:
        """Extract intent and create optimization request"""
        intent = self.intent_classifier.classify(prompt_input)
        
        # Analyze prompt structure
        output_type = self._determine_output_type(prompt_input)
        constraints = self._extract_constraints(prompt_input)
        missing_info = self._identify_missing_info(prompt_input, intent)
        
        return OptimizationRequest(
            raw_input=prompt_input,
            intent=intent,
            output_type=output_type,
            platform="claude",  # Default, will be overridden
            constraints=constraints,
            missing_info=missing_info
        )
    
    def apply_optimization(self, request: OptimizationRequest) -> Dict[str, Any]:
        """Apply 4-D optimization techniques"""
        optimization_data = {
            "original_prompt": request.raw_input,
            "intent": request.intent,
            "platform": request.platform,
            "improvements": [],
            "techniques_applied": []
        }
        
        # Deconstruct: Analyze prompt components
        components = self._deconstruct_prompt(request.raw_input)
        optimization_data["components"] = components
        
        # Develop: Enhance clarity and specificity
        developed_prompt = self.techniques.develop_clarity(
            request.raw_input, request.intent
        )
        if developed_prompt != request.raw_input:
            optimization_data["improvements"].append("Enhanced clarity and specificity")
            optimization_data["techniques_applied"].append("develop_clarity")
        
        # Design: Structure for target platform
        designed_prompt = self.techniques.design_structure(
            developed_prompt, request.platform, request.intent
        )
        if designed_prompt != developed_prompt:
            optimization_data["improvements"].append("Optimized structure for platform")
            optimization_data["techniques_applied"].append("design_structure")
        
        # Deliver: Final formatting and validation
        final_prompt = self.techniques.deliver_format(
            designed_prompt, request.output_type
        )
        if final_prompt != designed_prompt:
            optimization_data["improvements"].append("Applied final formatting")
            optimization_data["techniques_applied"].append("deliver_format")
        
        optimization_data["optimized_prompt"] = final_prompt
        
        return optimization_data
    
    def assemble_prompt(self, optimization_data: Dict[str, Any], 
                       request: OptimizationRequest) -> str:
        """Assemble the final optimized prompt"""
        return optimization_data.get("optimized_prompt", request.raw_input)
    
    def _determine_output_type(self, prompt: str) -> str:
        """Determine expected output type"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["list", "bullet", "enumerate"]):
            return "list"
        elif any(word in prompt_lower for word in ["explain", "describe", "tell"]):
            return "explanation"
        elif any(word in prompt_lower for word in ["code", "function", "script"]):
            return "code"
        elif any(word in prompt_lower for word in ["story", "narrative", "write"]):
            return "creative"
        else:
            return "general"
    
    def _extract_constraints(self, prompt: str) -> List[str]:
        """Extract explicit constraints from prompt"""
        constraints = []
        
        # Length constraints
        length_patterns = [
            r"(\d+)\s*words?",
            r"(\d+)\s*characters?",
            r"brief",
            r"detailed",
            r"short",
            r"long"
        ]
        
        for pattern in length_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                constraints.append(f"Length constraint: {pattern}")
        
        # Format constraints
        if re.search(r"json|yaml|xml", prompt, re.IGNORECASE):
            constraints.append("Structured format required")
        
        return constraints
    
    def _identify_missing_info(self, prompt: str, intent: str) -> List[str]:
        """Identify potentially missing information"""
        missing = []
        
        # Check for vague terms
        vague_terms = ["something", "anything", "stuff", "things", "it"]
        if any(term in prompt.lower() for term in vague_terms):
            missing.append("Vague references need clarification")
        
        # Check for missing context based on intent
        if intent == "technical" and not re.search(r"context|background|use case", 
                                                  prompt, re.IGNORECASE):
            missing.append("Technical context might be helpful")
        
        if intent == "creative" and not re.search(r"style|tone|audience", 
                                                 prompt, re.IGNORECASE):
            missing.append("Creative direction could be specified")
        
        return missing
    
    def _deconstruct_prompt(self, prompt: str) -> Dict[str, Any]:
        """Deconstruct prompt into components"""
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_questions": "?" in prompt,
            "has_examples": "example" in prompt.lower(),
            "complexity": "high" if len(prompt.split()) > 50 else "medium" if len(prompt.split()) > 20 else "low"
        }