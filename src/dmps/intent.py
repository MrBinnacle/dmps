"""
Intent detection and gap analysis for prompt optimization.
"""

import re
from typing import List


class IntentClassifier:
    """Classifies user intent from input text"""
    
    PATTERNS = {
        "creative": [
            "story", "creative", "generate", "imagine", "write", "poem", "fiction",
            "narrative", "character", "plot", "creative writing", "storytelling"
        ],
        "technical": [
            "code", "debug", "algorithm", "function", "API", "programming", "script",
            "software", "development", "bug", "error", "implement", "optimize"
        ],
        "educational": [
            "explain", "teach", "learn", "understand", "how", "what", "why", "tutorial",
            "lesson", "guide", "educational", "concept", "definition", "example"
        ],
        "complex": [
            "analyze", "compare", "evaluate", "strategy", "framework", "assess",
            "research", "report", "analysis", "comprehensive", "detailed", "thorough"
        ]
    }
    
    @classmethod
    def detect_intent(cls, text: str) -> str:
        """Detect primary intent from text"""
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in cls.PATTERNS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return "general"
        
        # Return intent with highest score
        return max(scores.items(), key=lambda x: x[1])[0]


class GapAnalyzer:
    """Analyzes missing information in prompts"""
    
    @classmethod
    def identify_gaps(cls, text: str, intent: str) -> List[str]:
        """Identify missing information based on text and intent"""
        gaps = []
        text_lower = text.lower()
        
        # Check for audience specification
        audience_indicators = ["audience", "reader", "user", "beginner", "expert", "professional"]
        if not any(indicator in text_lower for indicator in audience_indicators):
            gaps.append("audience")
        
        # Check for output format specification
        format_indicators = ["format", "structure", "list", "paragraph", "json", "table", "bullet"]
        if not any(indicator in text_lower for indicator in format_indicators):
            gaps.append("output_format")
        
        # Check for constraints
        constraint_indicators = ["length", "word", "character", "page", "limit", "constraint"]
        if not any(indicator in text_lower for indicator in constraint_indicators):
            gaps.append("constraints")
        
        # Intent-specific gap analysis
        if intent == "technical":
            tech_indicators = ["language", "framework", "version", "environment"]
            if not any(indicator in text_lower for indicator in tech_indicators):
                gaps.append("technical_context")
        
        elif intent == "creative":
            creative_indicators = ["tone", "style", "genre", "mood", "setting"]
            if not any(indicator in text_lower for indicator in creative_indicators):
                gaps.append("creative_context")
        
        elif intent == "educational":
            edu_indicators = ["level", "background", "prerequisite", "depth"]
            if not any(indicator in text_lower for indicator in edu_indicators):
                gaps.append("educational_context")
        
        return gaps
