"""
Tests for output formatters.
"""

import json
import pytest
from dmps.formatters import ConversationalFormatter, StructuredFormatter
from dmps.schema import OptimizationRequest


class TestConversationalFormatter:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.optimization_data = {
            "techniques_applied": ["role_assignment", "clear_structure"],
            "optimizations": {},
            "role": "You are an expert writer",
            "structure_guidance": "Use clear sections",
            "context_enhancements": "",
            "formatted_constraints": ""
        }
        
        self.request = OptimizationRequest(
            raw_input="Write a story",
            intent="creative",
            output_type="text",
            platform="claude",
            constraints=["500 words"],
            missing_info=["audience"]
        )
    
    def test_conversational_format(self):
        """Test conversational formatting"""
        result = ConversationalFormatter.format(
            self.optimization_data,
            self.request,
            "Your optimized prompt here"
        )
        
        assert result.format_type == "conversational"
        assert "**Your Optimized Prompt:**" in result.optimized_prompt
        assert "**What Changed:**" in result.optimized_prompt
        assert "Creative" in result.optimized_prompt
    
    def test_improvements_generation(self):
        """Test improvements list generation"""
        improvements = ConversationalFormatter._generate_improvements_list(
            ["role_assignment", "clear_structure"],
            ["audience"]
        )
        
        assert isinstance(improvements, list)
        assert len(improvements) > 0
        assert any("role" in imp.lower() for imp in improvements)
    
    def test_empty_improvements(self):
        """Test handling of no improvements"""
        formatted = ConversationalFormatter._format_improvements([])
        assert "already well-structured" in formatted


class TestStructuredFormatter:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.optimization_data = {
            "techniques_applied": ["role_assignment"],
            "optimizations": {},
            "role": "You are an expert",
            "structure_guidance": "Use sections",
            "context_enhancements": "",
            "formatted_constraints": ""
        }
        
        self.request = OptimizationRequest(
            raw_input="Test prompt",
            intent="general",
            output_type="text",
            platform="claude",
            constraints=[],
            missing_info=[]
        )
    
    def test_structured_format(self):
        """Test structured JSON formatting"""
        result = StructuredFormatter.format(
            self.optimization_data,
            self.request,
            "Optimized prompt"
        )
        
        assert result.format_type == "structured"
        
        # Parse JSON to verify structure
        data = json.loads(result.optimized_prompt)
        assert data["status"] == "success"
        assert "original_prompt" in data
        assert "optimized_prompt" in data
        assert "analysis" in data
        assert "optimization" in data
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        confidence = StructuredFormatter._calculate_confidence(self.optimization_data)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
    
    def test_metadata_generation(self):
        """Test metadata generation in structured format"""
        result = StructuredFormatter.format(
            self.optimization_data,
            self.request,
            "Test"
        )
        
        assert "confidence_score" in result.metadata
        assert "optimization_ratio" in result.metadata
        assert result.metadata["intent_detected"] == "general"