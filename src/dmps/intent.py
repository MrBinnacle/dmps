"""
Intent classification for prompt optimization.
"""

import re
from typing import Dict, List


class IntentClassifier:
    """Classifies prompt intent for optimization"""
    
    def __init__(self):
        self.intent_patterns = {
            "creative": [
                r"\b(write|create|generate|compose)\b.*\b(story|poem|article|content)\b",
                r"\b(creative|imaginative|artistic)\b",
                r"\b(character|plot|narrative|fiction)\b"
            ],
            "technical": [
                r"\b(code|program|function|algorithm|debug)\b",
                r"\b(technical|programming|software|development)\b",
                r"\b(api|database|server|framework)\b",
                r"\b(explain|how does|how to)\b.*\b(work|function|implement)\b"
            ],
            "educational": [
                r"\b(explain|teach|learn|understand|clarify)\b",
                r"\b(what is|define|definition|concept)\b",
                r"\b(tutorial|guide|instruction|lesson)\b",
                r"\b(example|demonstrate|show me)\b"
            ],
            "analytical": [
                r"\b(analyze|compare|evaluate|assess|review)\b",
                r"\b(pros and cons|advantages|disadvantages)\b",
                r"\b(data|statistics|research|study)\b",
                r"\b(conclusion|summary|findings)\b"
            ],
            "conversational": [
                r"\b(chat|talk|discuss|conversation)\b",
                r"\b(opinion|think|feel|believe)\b",
                r"\b(casual|friendly|informal)\b"
            ]
        }
    
    def classify(self, prompt: str) -> str:
        """Classify prompt intent"""
        prompt_lower = prompt.lower()
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, prompt_lower))
                score += matches
            scores[intent] = score
        
        # Return highest scoring intent, default to 'general'
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "general"
    
    def get_intent_keywords(self, intent: str) -> List[str]:
        """Get keywords associated with an intent"""
        keyword_map = {
            "creative": ["story", "creative", "write", "generate", "imaginative"],
            "technical": ["code", "technical", "program", "debug", "implement"],
            "educational": ["explain", "teach", "learn", "tutorial", "example"],
            "analytical": ["analyze", "compare", "evaluate", "data", "research"],
            "conversational": ["chat", "discuss", "opinion", "casual", "friendly"],
            "general": ["help", "assist", "provide", "give", "show"]
        }
        
        return keyword_map.get(intent, keyword_map["general"])