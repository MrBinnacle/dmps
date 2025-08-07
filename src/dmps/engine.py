"""
Core optimization engine implementing the 4-D methodology.
"""

import re
from typing import Any, Dict, Final, List

from .intent import IntentClassifier
from .schema import OptimizationRequest
from .techniques import OptimizationTechniques


class OptimizationEngine:
    """Core engine for prompt optimization using 4-D methodology"""

    # Constants for performance
    MAX_REGEX_INPUT: Final = 1000

    # Pre-compiled patterns
    _OUTPUT_PATTERNS = {
        "list": re.compile(r"\b(?:list|bullet|enumerate)\b", re.IGNORECASE),
        "explanation": re.compile(r"\b(?:explain|describe|tell)\b", re.IGNORECASE),
        "code": re.compile(r"\b(?:code|function|script)\b", re.IGNORECASE),
        "creative": re.compile(r"\b(?:story|narrative|write)\b", re.IGNORECASE),
    }

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.techniques = OptimizationTechniques()

    def extract_intent(self, prompt_input: str) -> OptimizationRequest:
        """Extract intent and create optimization request"""
        detected_intent = self.intent_classifier.classify(prompt_input)

        # Analyze prompt structure
        expected_format = self._determine_expected_output_format(prompt_input)
        user_constraints = self._extract_user_constraints(prompt_input)
        missing_info: List[str] = self._identify_missing_info(
            prompt_input, detected_intent
        )

        return OptimizationRequest(
            raw_input=prompt_input,
            intent=detected_intent,
            output_type=expected_format,
            platform="claude",  # Default, overridden by caller
            constraints=user_constraints,
            missing_info=missing_info,
        )

    def apply_optimization(self, request: OptimizationRequest) -> Dict[str, Any]:
        """Apply 4-D optimization techniques"""
        optimization_data = {
            "original_prompt": request.raw_input,
            "intent": request.intent,
            "platform": request.platform,
            "improvements": [],
            "techniques_applied": [],
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

    def assemble_prompt(
        self, optimization_data: Dict[str, Any], request: OptimizationRequest
    ) -> str:
        """Assemble the final optimized prompt"""
        return optimization_data.get("optimized_prompt", request.raw_input)

    def _determine_expected_output_format(self, user_prompt: str) -> str:
        """Analyze prompt to determine expected output format (list, code, etc.)"""
        # Truncate long prompts for performance
        analyzed_prompt = (
            user_prompt[: self.MAX_REGEX_INPUT]
            if len(user_prompt) > self.MAX_REGEX_INPUT
            else user_prompt
        )

        # Check for specific output format indicators
        for format_type, detection_pattern in self._OUTPUT_PATTERNS.items():
            if detection_pattern.search(analyzed_prompt):
                return format_type

        return "general"

    def _extract_user_constraints(self, user_prompt: str) -> List[str]:
        """Extract explicit user constraints (length, format, etc.) from prompt"""
        found_constraints = []

        # Limit input for safe regex processing
        safe_prompt = (
            user_prompt[: self.MAX_REGEX_INPUT]
            if len(user_prompt) > self.MAX_REGEX_INPUT
            else user_prompt
        )

        # Pre-compiled length patterns for performance
        length_patterns = [
            re.compile(r"\b\d{1,4}\s*words?\b", re.IGNORECASE),
            re.compile(r"\b\d{1,4}\s*characters?\b", re.IGNORECASE),
            re.compile(r"\bbrief\b", re.IGNORECASE),
            re.compile(r"\bdetailed\b", re.IGNORECASE),
            re.compile(r"\bshort\b", re.IGNORECASE),
            re.compile(r"\blong\b", re.IGNORECASE),
        ]

        for pattern in length_patterns:
            try:
                if pattern.search(safe_prompt):
                    found_constraints.append("Length constraint found")
                    break  # Only need to find one
            except re.error:
                continue

        # Format constraints
        try:
            if re.search(r"\b(?:json|yaml|xml)\b", safe_prompt, re.IGNORECASE):
                found_constraints.append("Structured format required")
        except re.error:
            pass

        return found_constraints

    def _identify_missing_info(self, prompt: str, intent: str) -> List[str]:
        """Identify potentially missing information with safe regex"""
        missing = []

        # Limit input length
        if len(prompt) > self.MAX_REGEX_INPUT:
            prompt = prompt[: self.MAX_REGEX_INPUT]

        prompt_lower = prompt.lower()

        # Check for vague terms (simple string matching)
        vague_terms = ["something", "anything", "stuff", "things"]
        if any(term in prompt_lower for term in vague_terms):
            missing.append("Vague references need clarification")

        # Check for missing context based on intent (safe regex)
        try:
            if intent == "technical" and not re.search(
                r"\b(?:context|background|use case)\b", prompt, re.IGNORECASE
            ):
                missing.append("Technical context might be helpful")

            if intent == "creative" and not re.search(
                r"\b(?:style|tone|audience)\b", prompt, re.IGNORECASE
            ):
                missing.append("Creative direction could be specified")
        except re.error:
            pass

        return missing

    def _deconstruct_prompt(self, prompt: str) -> Dict[str, Any]:
        """Deconstruct prompt into components"""
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_questions": "?" in prompt,
            "has_examples": "example" in prompt.lower(),
            "complexity": (
                "high"
                if len(prompt.split()) > 50
                else "medium"
                if len(prompt.split()) > 20
                else "low"
            ),
        }
