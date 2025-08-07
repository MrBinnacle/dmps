"""
Intent classification for prompt optimization.
"""

import re


class IntentClassifier:
    """Classifies prompt intent for optimization"""

    def __init__(self):
        # Pre-compiled patterns for performance
        self.compiled_patterns = {
            "creative": [
                re.compile(
                    r"\b(write|create|generate|compose)\b.*\b(story|poem|article|content)\b",
                    re.IGNORECASE,
                ),
                re.compile(r"\b(creative|imaginative|artistic)\b", re.IGNORECASE),
                re.compile(r"\b(character|plot|narrative|fiction)\b", re.IGNORECASE),
            ],
            "technical": [
                re.compile(
                    r"\b(code|program|function|algorithm|debug)\b", re.IGNORECASE
                ),
                re.compile(
                    r"\b(technical|programming|software|development)\b", re.IGNORECASE
                ),
                re.compile(r"\b(api|database|server|framework)\b", re.IGNORECASE),
                re.compile(
                    r"\b(explain|how does|how to)\b.*\b(work|function|implement)\b",
                    re.IGNORECASE,
                ),
            ],
            "educational": [
                re.compile(
                    r"\b(explain|teach|learn|understand|clarify)\b", re.IGNORECASE
                ),
                re.compile(r"\b(what is|define|definition|concept)\b", re.IGNORECASE),
                re.compile(r"\b(tutorial|guide|instruction|lesson)\b", re.IGNORECASE),
                re.compile(r"\b(example|demonstrate|show me)\b", re.IGNORECASE),
            ],
            "analytical": [
                re.compile(
                    r"\b(analyze|compare|evaluate|assess|review)\b", re.IGNORECASE
                ),
                re.compile(
                    r"\b(pros and cons|advantages|disadvantages)\b", re.IGNORECASE
                ),
                re.compile(r"\b(data|statistics|research|study)\b", re.IGNORECASE),
                re.compile(r"\b(conclusion|summary|findings)\b", re.IGNORECASE),
            ],
            "conversational": [
                re.compile(r"\b(chat|talk|discuss|conversation)\b", re.IGNORECASE),
                re.compile(r"\b(opinion|think|feel|believe)\b", re.IGNORECASE),
                re.compile(r"\b(casual|friendly|informal)\b", re.IGNORECASE),
            ],
        }

    def classify(self, prompt: str) -> str:
        """Classify prompt intent using compiled patterns with performance monitoring"""
        from .profiler import performance_monitor

        @performance_monitor(threshold=0.05)
        def _classify_with_monitoring():
            scores = {}

            for intent, patterns in self.compiled_patterns.items():
                score = 0
                for pattern in patterns:
                    matches = len(pattern.findall(prompt))
                    score += matches
                scores[intent] = score

            # Return highest scoring intent, default to 'general'
            if scores:
                max_score = max(scores.values())
                if max_score > 0:
                    # Use a lambda for key to avoid overload issues
                    return max(scores, key=lambda k: scores[k])
                return "general"

        return _classify_with_monitoring()

    # Static keyword mapping for performance
    _KEYWORD_MAP = {
        "creative": ["story", "creative", "write", "generate", "imaginative"],
        "technical": ["code", "technical", "program", "debug", "implement"],
        "educational": ["explain", "teach", "learn", "tutorial", "example"],
        "analytical": ["analyze", "compare", "evaluate", "data", "research"],
        "conversational": ["chat", "discuss", "opinion", "casual", "friendly"],
        "general": ["help", "assist", "provide", "give", "show"],
    }

    def get_intent_keywords(self, intent: str) -> "list[str]":
        """Get keywords associated with an intent"""
        return self._KEYWORD_MAP.get(intent, self._KEYWORD_MAP["general"])
