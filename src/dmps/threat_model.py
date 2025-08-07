"""
Threat modeling and security controls for DMPS.
"""

from enum import Enum
from typing import Dict, Final, List


class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatModel:
    """DMPS threat model and mitigations"""

    THREATS: Final[Dict[str, Dict]] = {
        "path_traversal": {
            "level": ThreatLevel.CRITICAL,
            "description": "Directory traversal via file operations",
            "mitigations": ["path_validation", "sandboxing", "input_sanitization"],
            "affected_components": ["cli.py", "repl.py"],
        },
        "authorization_bypass": {
            "level": ThreatLevel.HIGH,
            "description": "Unauthorized command execution",
            "mitigations": ["command_whitelist", "input_validation", "rbac"],
            "affected_components": ["repl.py", "techniques.py"],
        },
        "injection_attacks": {
            "level": ThreatLevel.HIGH,
            "description": "Code/script injection via user input",
            "mitigations": [
                "input_sanitization",
                "pattern_blocking",
                "output_encoding",
            ],
            "affected_components": ["validation.py", "engine.py"],
        },
    }

    @classmethod
    def get_critical_threats(cls) -> List[str]:
        """Get list of critical threats"""
        return [
            name
            for name, threat in cls.THREATS.items()
            if threat["level"] == ThreatLevel.CRITICAL
        ]

    @classmethod
    def validate_mitigations(cls) -> bool:
        """Validate all critical mitigations are in place"""
        from .security import SecurityConfig

        # Check path traversal mitigations
        if SecurityConfig.is_safe_path("../../../etc/passwd"):
            return False

        # Check input sanitization
        from .validation import InputValidator

        validator = InputValidator()
        result = validator.validate_input("<script>alert('xss')</script>")
        if not result.warnings:
            return False

        return True
