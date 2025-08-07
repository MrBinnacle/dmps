"""
Secure error handling with graceful degradation.
"""

import logging
from enum import Enum
from typing import Any, Optional


class ErrorLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SecureErrorHandler:
    """Secure error handling with information leak prevention"""

    def __init__(self):
        # Configure secure logging
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("dmps_errors.log")],
        )
        self.logger = logging.getLogger(__name__)

    def handle_error(
        self, error: Exception, context: str = "", user_message: Optional[str] = None
    ) -> str:
        """Enhanced error handling with actionable messages"""

        # Log with structured context for debugging
        error_details = {
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        self.logger.error(f"Error occurred: {error_details}", exc_info=True)

        if user_message:
            return user_message

        # Actionable error messages for debugging
        actionable_messages = {
            FileNotFoundError: "File not found. Check the file path and ensure it exists.",
            PermissionError: "Access denied. Verify file permissions and path validity.",
            ValueError: "Invalid input. Please check your input format and try again.",
            OSError: "System operation failed. Check disk space and file permissions.",
            ImportError: "Module import failed. Ensure all dependencies are installed.",
            TypeError: "Type mismatch. Check input data types.",
            KeyError: "Missing required key. Check configuration or input data.",
            Exception: "An unexpected error occurred. Check logs for details.",
        }

        return actionable_messages.get(
            type(error), "An unexpected error occurred. Check logs for details."
        )

    def handle_security_error(self, error: Exception, context: str = "") -> str:
        """Enhanced security error handling with detailed logging"""
        security_context = {
            "security_event": True,
            "context": context,
            "error_type": type(error).__name__,
            "timestamp": self._get_timestamp(),
        }
        self.logger.critical(f"SECURITY VIOLATION: {security_context}")

        # Provide actionable security messages
        security_messages = {
            PermissionError: "Access denied. Operation blocked for security.",
            ValueError: "Invalid input detected. Security validation failed.",
            OSError: "File operation blocked. Path validation failed.",
        }

        return security_messages.get(
            type(error), "Security validation failed. Operation blocked."
        )

    def graceful_degradation(
        self, fallback_value: Any, error: Exception, context: str = ""
    ) -> Any:
        """Provide graceful degradation with fallback"""
        self.logger.warning(f"Degradation: {context}, Error: {str(error)}")
        return fallback_value

    def _get_timestamp(self) -> str:
        """Get formatted timestamp for logging"""
        from datetime import datetime

        return datetime.now().isoformat()

    def log_performance_issue(
        self, operation: str, duration: float, threshold: float = 1.0
    ):
        """Log performance issues for monitoring"""
        if duration > threshold:
            self.logger.warning(
                f"Performance issue: {operation} took {
                    duration:.2f}s (threshold: {threshold}s)"
            )


# Global error handler instance
error_handler = SecureErrorHandler()
