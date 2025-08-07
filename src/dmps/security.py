"""
Security configuration and utilities for DMPS.
"""

import os
import re
from pathlib import Path
from typing import Dict, Final


class SecurityConfig:
    """Centralized security configuration"""

    # File operation limits
    MAX_FILE_SIZE: Final = 1024 * 1024  # 1MB
    MAX_INPUT_LENGTH: Final = 10000
    MAX_LINES: Final = 100

    # Rate limiting
    MAX_REQUESTS_PER_SESSION: Final = 1000
    MAX_HISTORY_SIZE: Final = 100

    # Allowed file extensions for save operations
    ALLOWED_EXTENSIONS: Final["frozenset[str]"] = frozenset({".json", ".txt"})

    # Pre-compiled patterns for better performance
    _COMPILED_PATTERNS = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"data:text/html", re.IGNORECASE),
        re.compile(r"file://", re.IGNORECASE),
        re.compile(r"\.\./", re.IGNORECASE),
        re.compile(r"\\\.\.\\", re.IGNORECASE),
        re.compile(r"eval\s*\(", re.IGNORECASE),
        re.compile(r"exec\s*\(", re.IGNORECASE),
        re.compile(r"__import__\s*\(", re.IGNORECASE),
    ]

    # Pre-compiled dangerous patterns for O(1) lookup
    _DANGEROUS_PATTERNS: Final = frozenset(
        ["..", "~", "/etc/", "/root/", "C:\\Windows", "C:\\Users"]
    )

    @classmethod
    def validate_file_path(cls, filepath: str) -> bool:
        """Validate file path for compatibility with legacy code."""
        return cls.is_safe_path(filepath)

    @classmethod
    def is_safe_path(cls, filepath: str) -> bool:
        """Optimized path safety check with pattern matching"""
        try:
            # Fast pattern matching with frozenset
            if any(pattern in filepath for pattern in cls._DANGEROUS_PATTERNS):
                return False

            path = Path(filepath).resolve()
            cwd = Path.cwd().resolve()

            # Sandboxing: only allow within current directory
            try:
                path.relative_to(cwd)
                return True
            except ValueError:
                return False

        except (OSError, ValueError):
            return False

    @classmethod
    def validate_file_extension(cls, filepath: str) -> bool:
        """Validate file extension is allowed"""
        return Path(filepath).suffix.lower() in cls.ALLOWED_EXTENSIONS

    @classmethod
    def get_compiled_patterns(cls):
        """Get cached compiled patterns"""
        return cls._COMPILED_PATTERNS

    @classmethod
    def validate_multiple_paths(cls, filepaths: list) -> Dict[str, bool]:
        """Batch validate multiple paths for better performance"""
        return {path: cls.is_safe_path(path) for path in filepaths}

    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize filename to prevent issues"""
        # Remove dangerous characters
        dangerous_chars = '<>:"|?*\\'
        for char in dangerous_chars:
            filename = filename.replace(char, "_")

        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext

        return filename
