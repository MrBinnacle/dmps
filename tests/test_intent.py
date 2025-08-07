"""
Tests for intent detection and gap analysis.
"""

import pytest
from dmps.intent import IntentClassifier


class TestIntentClassifier:
    
    def test_creative_intent_detection(self):
        """Test detection of creative intent"""
        text = "Write a creative story about a robot"
        intent = IntentClassifier.detect_intent(text)
        assert intent == "creative"
    
    def test_technical_intent_detection(self):
        """Test detection of technical intent"""
        text = "Debug this Python code function"
        intent = IntentClassifier.detect_intent(text)
        assert intent == "technical"
    
    def test_educational_intent_detection(self):
        """Test detection of educational intent"""
        text = "Explain how neural networks work"
        intent = IntentClassifier.detect_intent(text)
        assert intent == "educational"
    
    def test_complex_intent_detection(self):
        """Test detection of complex analysis intent"""
        text = "Analyze the market strategy and compare competitors"
        intent = IntentClassifier.detect_intent(text)
        assert intent == "complex"
    
    def test_general_intent_fallback(self):
        """Test fallback to general intent"""
        text = "Hello there"
        intent = IntentClassifier.detect_intent(text)
        assert intent == "general"
    
    def test_mixed_keywords(self):
        """Test handling of mixed keywords"""
        text = "Write code to explain algorithms creatively"
        intent = IntentClassifier.detect_intent(text)
        # Should pick the intent with highest score
        assert intent in ["creative", "technical", "educational"]


class TestGapAnalyzer:
    
    def test_audience_gap_detection(self):
        """Test detection of missing audience specification"""
        text = "Explain quantum computing"
        gaps = GapAnalyzer.identify_gaps(text, "educational")
        assert "audience" in gaps
    
    def test_format_gap_detection(self):
        """Test detection of missing format specification"""
        text = "Tell me about AI"
        gaps = GapAnalyzer.identify_gaps(text, "general")
        assert "output_format" in gaps
    
    def test_constraints_gap_detection(self):
        """Test detection of missing constraints"""
        text = "Write something"
        gaps = GapAnalyzer.identify_gaps(text, "creative")
        assert "constraints" in gaps
    
    def test_technical_context_gap(self):
        """Test detection of missing technical context"""
        text = "Write code"
        gaps = GapAnalyzer.identify_gaps(text, "technical")
        assert "technical_context" in gaps
    
    def test_creative_context_gap(self):
        """Test detection of missing creative context"""
        text = "Write a story"
        gaps = GapAnalyzer.identify_gaps(text, "creative")
        assert "creative_context" in gaps
    
    def test_no_gaps_when_complete(self):
        """Test that well-specified prompts have fewer gaps"""
        text = "Write a 500-word professional blog post for developers about Python list comprehensions in bullet format"
        gaps = GapAnalyzer.identify_gaps(text, "technical")
        # Should have fewer gaps due to specificity
        assert len(gaps) < 4