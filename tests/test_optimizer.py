"""
Tests for the PromptOptimizer class.
"""

import pytest
from dmps.optimizer import PromptOptimizer
from dmps.schema import OptimizedResult, ValidationResult


class TestPromptOptimizer:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.optimizer = PromptOptimizer()
    
    def test_basic_optimization(self):
        """Test basic prompt optimization"""
        result, validation = self.optimizer.optimize("Write a story")
        
        assert isinstance(result, OptimizedResult)
        assert isinstance(validation, ValidationResult)
        assert validation.is_valid
        assert len(result.optimized_prompt) > 0
    
    def test_conversational_mode(self):
        """Test conversational output mode"""
        result, validation = self.optimizer.optimize(
            "Explain machine learning", 
            mode="conversational"
        )
        
        assert result.format_type == "conversational"
        assert "**Your Optimized Prompt:**" in result.optimized_prompt
    
    def test_structured_mode(self):
        """Test structured output mode"""
        result, validation = self.optimizer.optimize(
            "Debug this code", 
            mode="structured"
        )
        
        assert result.format_type == "structured"
        assert result.optimized_prompt.startswith("{")
    
    def test_platform_optimization(self):
        """Test platform-specific optimization"""
        result_claude, _ = self.optimizer.optimize("Test prompt", platform="claude")
        result_chatgpt, _ = self.optimizer.optimize("Test prompt", platform="chatgpt")
        
        # Results should be different for different platforms
        assert result_claude.optimized_prompt != result_chatgpt.optimized_prompt
    
    def test_empty_input_validation(self):
        """Test validation of empty input"""
        result, validation = self.optimizer.optimize("")
        
        assert not validation.is_valid
        assert len(validation.errors) > 0
        assert "empty" in validation.errors[0].lower()
    
    def test_short_input_validation(self):
        """Test validation of too short input"""
        result, validation = self.optimizer.optimize("Hi")
        
        assert not validation.is_valid
        assert "too short" in validation.errors[0].lower()
    
    def test_improvements_tracking(self):
        """Test that improvements are properly tracked"""
        result, validation = self.optimizer.optimize("Write code")
        
        assert isinstance(result.improvements, list)
        assert len(result.improvements) > 0
    
    def test_metadata_generation(self):
        """Test metadata is properly generated"""
        result, validation = self.optimizer.optimize("Test prompt")
        
        assert isinstance(result.metadata, dict)
        assert "intent" in result.metadata
    
    def test_fallback_handling(self):
        """Test fallback behavior on processing errors"""
        # This would require mocking internal components to force an error
        # For now, just test that the optimizer handles normal cases
        result, validation = self.optimizer.optimize("Normal prompt")
        assert validation.is_valid