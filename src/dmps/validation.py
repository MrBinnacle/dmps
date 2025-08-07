"""
Input validation and sanitization for DMPS.
"""

import re
from typing import List
from .schema import ValidationResult


class InputValidator:
    """Validates and sanitizes input"""
    
    MIN_LENGTH = 5
    MAX_LENGTH = 10000
    
    @classmethod
    def validate_input(cls, prompt_input: str, mode: str = "conversational") -> ValidationResult:
        """Comprehensive input validation"""
        errors = []
        warnings = []
        sanitized_input = prompt_input.strip()
        
        # Basic validation
        if not prompt_input or not prompt_input.strip():
            errors.append("Input cannot be empty")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                sanitized_input=None
            )
        
        # Length validation
        if len(sanitized_input) < cls.MIN_LENGTH:
            errors.append(f"Input too short (minimum {cls.MIN_LENGTH} characters)")
        
        if len(sanitized_input) > cls.MAX_LENGTH:
            errors.append(f"Input too long (maximum {cls.MAX_LENGTH} characters)")
        
        # Mode validation
        if mode not in ["conversational", "structured"]:
            errors.append(f"Invalid mode: {mode}. Must be 'conversational' or 'structured'")
        
        # Content validation
        if cls._contains_suspicious_content(sanitized_input):
            warnings.append("Input contains potentially problematic content")
        
        # Sanitization
        sanitized_input = cls._sanitize_input(sanitized_input)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_input=sanitized_input
        )
    
    @classmethod
    def _contains_suspicious_content(cls, text: str) -> bool:
        """Check for potentially problematic content"""
        suspicious_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'data:text/html',
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL) 
                  for pattern in suspicious_patterns)
    
    @classmethod
    def _sanitize_input(cls, text: str) -> str:
        """Sanitize input text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove potential HTML/script tags
        text = re.sub(r'<[^>]*>', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
