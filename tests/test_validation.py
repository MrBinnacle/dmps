"""
Tests for input validation.
"""

import pytest
from dmps.validation import InputValidator


class TestInputValidator:
    
    def test_valid_input(self):
        """Test validation of valid input"""
        result = InputValidator.validate_input("This is a valid prompt for testing")
        
        assert result.is_valid
        assert len(result.errors) == 0
        assert result.sanitized_input is not None
    
    def test_empty_input(self):
        """Test validation of empty input"""
        result = InputValidator.validate_input("")
        
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()
    
    def test_whitespace_only_input(self):
        """Test validation of whitespace-only input"""
        result = InputValidator.validate_input("   \n\t   ")
        
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()
    
    def test_too_short_input(self):
        """Test validation of too short input"""
        result = InputValidator.validate_input("Hi")
        
        assert not result.is_valid
        assert "too short" in result.errors[0].lower()
    
    def test_too_long_input(self):
        """Test validation of too long input"""
        long_input = "x" * 15000  # Exceeds MAX_LENGTH
        result = InputValidator.validate_input(long_input)
        
        assert not result.is_valid
        assert "too long" in result.errors[0].lower()
    
    def test_invalid_mode(self):
        """Test validation with invalid mode"""
        result = InputValidator.validate_input("Valid prompt", mode="invalid_mode")
        
        assert not result.is_valid
        assert "invalid mode" in result.errors[0].lower()
    
    def test_suspicious_content_detection(self):
        """Test detection of suspicious content"""
        suspicious_input = "This prompt contains <script>alert('test')</script> content"
        result = InputValidator.validate_input(suspicious_input)
        
        # Should still be valid but with warnings
        assert result.is_valid
        assert len(result.warnings) > 0
        assert "problematic content" in result.warnings[0].lower()
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        messy_input = "  This   has    excessive   whitespace  \n\n  "
        result = InputValidator.validate_input(messy_input)
        
        assert result.is_valid
        assert result.sanitized_input.count(" ") < messy_input.count(" ")
    
    def test_html_tag_removal(self):
        """Test HTML tag removal during sanitization"""
        html_input = "This has <b>bold</b> and <i>italic</i> tags"
        result = InputValidator.validate_input(html_input)
        
        assert result.is_valid
        assert "<b>" not in result.sanitized_input
        assert "<i>" not in result.sanitized_input
        assert "bold" in result.sanitized_input
        assert "italic" in result.sanitized_input
    
    def test_quote_normalization(self):
        """Test quote normalization during sanitization"""
        quote_input = "This has \"smart quotes\" and 'curly apostrophes'"
        result = InputValidator.validate_input(quote_input)
        
        assert result.is_valid
        assert '"' in result.sanitized_input
        assert "'" in result.sanitized_input