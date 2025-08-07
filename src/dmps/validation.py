"""
Input validation and sanitization for DMPS.
"""

import re
from typing import Final, List

from .schema import ValidationResult
from .security import SecurityConfig


class InputValidator:
    """Validates and sanitizes input with security controls"""

    MIN_LENGTH: Final = 5
    MAX_LENGTH: Final = SecurityConfig.MAX_INPUT_LENGTH
    MAX_LINES: Final = SecurityConfig.MAX_LINES

    # Pre-compiled patterns for performance
    _WHITESPACE_PATTERN = re.compile(r"[ \t]+")
    _NEWLINE_PATTERN = re.compile(r"\n\s*\n\s*\n+")
    _HTML_PATTERN = re.compile(r"<[^>]*>")
    _PATH_PATTERN = re.compile(r"\.\.[\\/]")
    _CODE_PATTERN = re.compile(r"\b(eval|exec|__import__)\s*\(", re.IGNORECASE)

    @classmethod
    def validate_input(
        cls, prompt_input: str, mode: str = "conversational"
    ) -> ValidationResult:
        """Comprehensive input validation"""
        errors = []
        warnings: List[str] = []
        sanitized_input = prompt_input.strip()

        # Basic validation
        if not prompt_input or not prompt_input.strip():
            errors.append("Input cannot be empty")
            return ValidationResult(
                is_valid=False, errors=errors, warnings=warnings, sanitized_input=None
            )

        # Length validation
        if len(sanitized_input) < cls.MIN_LENGTH:
            errors.append(f"Input too short (minimum {cls.MIN_LENGTH} characters)")

        if len(sanitized_input) > cls.MAX_LENGTH:
            errors.append(f"Input too long (maximum {cls.MAX_LENGTH} characters)")

        # Line count validation (DoS prevention)
        line_count = len(sanitized_input.splitlines())
        if line_count > cls.MAX_LINES:
            errors.append(f"Too many lines (maximum {cls.MAX_LINES} lines)")

        # Mode validation
        if mode not in ["conversational", "structured"]:
            errors.append(
                f"Invalid mode: {mode}. Must be 'conversational' or 'structured'"
            )

        # Content validation
        if cls._contains_suspicious_content(sanitized_input):
            warnings.append("Input contains potentially problematic content")

        # Sanitization
        sanitized_input = cls._sanitize_input(sanitized_input)

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_input=sanitized_input,
        )

    @classmethod
    def _contains_suspicious_content(cls, text: str) -> bool:
        """Check for potentially problematic content"""
        text_lower = text.lower()

        for pattern in SecurityConfig.get_compiled_patterns():
            try:
                if pattern.search(text_lower):
                    return True
            except (re.error, AttributeError):
                continue

        return False

    @classmethod
    def _sanitize_input(cls, text: str) -> str:
        """Sanitize input text with enhanced security"""
        # Remove excessive whitespace but preserve line breaks
        text = cls._WHITESPACE_PATTERN.sub(" ", text)
        text = cls._NEWLINE_PATTERN.sub("\n\n", text)

        # Remove potential HTML/script tags
        text = cls._HTML_PATTERN.sub("", text)

        # Remove potential path traversal sequences
        text = cls._PATH_PATTERN.sub("", text)

        # Remove potential code injection patterns
        text = cls._CODE_PATTERN.sub("", text)

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(""", "'").replace(""", "'")

        # Remove null bytes and control characters (except newlines and tabs)
        text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")

        return text.strip()
