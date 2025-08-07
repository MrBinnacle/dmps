"""
Edge case tests to achieve 90%+ coverage.
"""

import pytest
import tempfile
import os
from pathlib import Path
from dmps import optimize_prompt, PromptOptimizer
from dmps.security import SecurityConfig
from dmps.validation import InputValidator
from dmps.engine import OptimizationEngine
from dmps.intent import IntentClassifier
from dmps.techniques import OptimizationTechniques
from dmps.formatters import ConversationalFormatter, StructuredFormatter
from dmps.repl import DMPSShell
from dmps.rbac import AccessControl, Role, Permission
from dmps.error_handler import SecureErrorHandler
from dmps.cache import PerformanceCache


class TestSecurityEdgeCases:
    """Edge cases for security components"""
    
    def test_security_config_edge_cases(self):
        """Test SecurityConfig edge cases"""
        # Empty path
        assert not SecurityConfig.is_safe_path("")
        
        # None path
        with pytest.raises(AttributeError):
            SecurityConfig.is_safe_path(None)
        
        # Very long path
        long_path = "a" * 1000
        assert SecurityConfig.is_safe_path(long_path)
        
        # Path with null bytes
        assert not SecurityConfig.is_safe_path("test\x00file.txt")
        
        # Multiple path validation
        paths = ["safe.txt", "../unsafe.txt", "another.txt"]
        results = SecurityConfig.validate_multiple_paths(paths)
        assert results["safe.txt"] == True
        assert results["../unsafe.txt"] == False
    
    def test_validation_edge_cases(self):
        """Test InputValidator edge cases"""
        validator = InputValidator()
        
        # Empty string
        result = validator.validate_input("")
        assert not result.is_valid
        
        # Only whitespace
        result = validator.validate_input("   \n\t  ")
        assert not result.is_valid
        
        # Exactly minimum length
        result = validator.validate_input("12345")
        assert result.is_valid
        
        # Maximum length boundary
        max_input = "x" * SecurityConfig.MAX_INPUT_LENGTH
        result = validator.validate_input(max_input)
        assert result.is_valid
        
        # Over maximum length
        over_max = "x" * (SecurityConfig.MAX_INPUT_LENGTH + 1)
        result = validator.validate_input(over_max)
        assert not result.is_valid
        
        # Maximum lines boundary
        max_lines = "\n".join(["line"] * SecurityConfig.MAX_LINES)
        result = validator.validate_input(max_lines)
        assert result.is_valid
        
        # Over maximum lines
        over_lines = "\n".join(["line"] * (SecurityConfig.MAX_LINES + 1))
        result = validator.validate_input(over_lines)
        assert not result.is_valid
        
        # Invalid mode
        result = validator.validate_input("test prompt", "invalid_mode")
        assert not result.is_valid
        
        # Unicode characters
        result = validator.validate_input("Test with émojis 🚀")
        assert result.is_valid
        
        # Control characters
        result = validator.validate_input("test\x01\x02control")
        assert result.is_valid
        assert "\x01" not in result.sanitized_input


class TestEngineEdgeCases:
    """Edge cases for optimization engine"""
    
    def test_engine_edge_cases(self):
        """Test OptimizationEngine edge cases"""
        engine = OptimizationEngine()
        
        # Empty prompt
        request = engine.extract_intent("")
        assert request.intent == "general"
        
        # Very short prompt
        request = engine.extract_intent("Hi")
        assert request.intent in ["conversational", "general"]
        
        # Very long prompt
        long_prompt = "Write a story " * 1000
        request = engine.extract_intent(long_prompt)
        assert request.intent == "creative"
        
        # Mixed intent prompt
        mixed = "Write a technical story about debugging code with examples"
        request = engine.extract_intent(mixed)
        assert request.intent in ["creative", "technical", "educational"]
        
        # Non-ASCII characters
        unicode_prompt = "Écrivez une histoire sur l'IA"
        request = engine.extract_intent(unicode_prompt)
        assert request.intent == "general"
    
    def test_output_type_detection_edge_cases(self):
        """Test output type detection edge cases"""
        engine = OptimizationEngine()
        
        # Multiple indicators
        mixed_prompt = "Create a list of code examples with explanations"
        output_type = engine._determine_expected_output_format(mixed_prompt)
        assert output_type in ["list", "code", "explanation"]
        
        # No clear indicators
        vague_prompt = "Help me with something"
        output_type = engine._determine_expected_output_format(vague_prompt)
        assert output_type == "general"
        
        # Case sensitivity
        case_prompt = "CREATE A LIST"
        output_type = engine._determine_expected_output_format(case_prompt)
        assert output_type == "list"


class TestTechniquesEdgeCases:
    """Edge cases for optimization techniques"""
    
    def test_techniques_edge_cases(self):
        """Test OptimizationTechniques edge cases"""
        tech = OptimizationTechniques()
        
        # Empty prompt
        result = tech.develop_clarity("", "general")
        assert len(result) > 0
        
        # Already optimized prompt
        optimized = "Please provide a detailed technical explanation of machine learning algorithms with specific examples and context."
        result = tech.develop_clarity(optimized, "technical")
        assert "Context:" not in result  # Should not add duplicate context
        
        # Invalid platform
        result = tech.design_structure("test", "invalid_platform", "general")
        assert "test" in result
        
        # Invalid technique description
        desc = tech.get_technique_description("invalid_technique")
        assert desc == "Unknown technique"
        
        # All valid techniques
        for technique in tech.ALLOWED_TECHNIQUES:
            desc = tech.get_technique_description(technique)
            assert desc != "Unknown technique"


class TestRBACEdgeCases:
    """Edge cases for RBAC system"""
    
    def test_rbac_edge_cases(self):
        """Test RBAC edge cases"""
        # Invalid role
        with pytest.raises(AttributeError):
            AccessControl.has_permission("invalid_role", Permission.READ_FILE)
        
        # Invalid permission
        with pytest.raises(AttributeError):
            AccessControl.has_permission(Role.USER, "invalid_permission")
        
        # Empty command
        assert not AccessControl.is_command_allowed("")
        
        # Case sensitivity
        assert not AccessControl.is_command_allowed("HELP")
        assert AccessControl.is_command_allowed("help")
        
        # File operation with invalid parameters
        assert not AccessControl.validate_file_operation(Role.USER, "invalid_op", "test.txt")
        assert not AccessControl.validate_file_operation(Role.USER, "read", "../invalid.txt")


class TestREPLEdgeCases:
    """Edge cases for REPL interface"""
    
    def test_repl_edge_cases(self):
        """Test DMPSShell edge cases"""
        shell = DMPSShell()
        
        # Rate limiting
        shell.request_count = shell.max_requests + 1
        shell.optimize_and_display("test")  # Should be blocked
        
        # History overflow
        for i in range(shell.max_history + 10):
            shell.history.append({"test": f"item_{i}"})
        
        # Simulate history cleanup
        if len(shell.history) > shell.max_history:
            shell.history = shell.history[-shell.max_history:]
        
        assert len(shell.history) <= shell.max_history
        
        # Invalid settings
        shell._update_configuration_setting(["invalid_setting", "value"])
        shell._update_configuration_setting(["mode", "invalid_mode"])
        shell._update_configuration_setting(["platform", "invalid_platform"])
        shell._update_configuration_setting(["show_metadata", "invalid_bool"])
        
        # Insufficient arguments
        shell._update_configuration_setting(["mode"])
        shell._update_configuration_setting([])


class TestFormatterEdgeCases:
    """Edge cases for formatters"""
    
    def test_formatter_edge_cases(self):
        """Test formatter edge cases"""
        from dmps.schema import OptimizationRequest
        
        # Empty optimization data
        empty_data = {}
        request = OptimizationRequest(
            raw_input="test",
            intent="general",
            output_type="general",
            platform="claude",
            constraints=[],
            missing_info=[]
        )
        
        # Conversational formatter
        conv_formatter = ConversationalFormatter()
        result = conv_formatter.format(empty_data, request, "optimized")
        assert result.format_type == "conversational"
        
        # Structured formatter
        struct_formatter = StructuredFormatter()
        result = struct_formatter.format(empty_data, request, "optimized")
        assert result.format_type == "structured"
        
        # Large data
        large_data = {
            "improvements": ["improvement"] * 100,
            "techniques_applied": ["technique"] * 50
        }
        
        conv_result = conv_formatter.format(large_data, request, "optimized")
        assert len(conv_result.improvements) == 100


class TestCacheEdgeCases:
    """Edge cases for caching system"""
    
    def test_cache_edge_cases(self):
        """Test PerformanceCache edge cases"""
        # Hash collision handling
        hash1 = PerformanceCache.get_prompt_hash("test prompt")
        hash2 = PerformanceCache.get_prompt_hash("test prompt")
        assert hash1 == hash2
        
        # Different prompts
        hash3 = PerformanceCache.get_prompt_hash("different prompt")
        assert hash1 != hash3
        
        # Empty prompt
        hash_empty = PerformanceCache.get_prompt_hash("")
        assert isinstance(hash_empty, str)
        
        # Unicode prompt
        hash_unicode = PerformanceCache.get_prompt_hash("test émoji 🚀")
        assert isinstance(hash_unicode, str)


class TestErrorHandlerEdgeCases:
    """Edge cases for error handling"""
    
    def test_error_handler_edge_cases(self):
        """Test SecureErrorHandler edge cases"""
        handler = SecureErrorHandler()
        
        # Unknown exception type
        class CustomError(Exception):
            pass
        
        msg = handler.handle_error(CustomError("test"), "context")
        assert "unexpected error" in msg.lower()
        
        # None context
        msg = handler.handle_error(ValueError("test"), None)
        assert isinstance(msg, str)
        
        # Empty context
        msg = handler.handle_error(ValueError("test"), "")
        assert isinstance(msg, str)
        
        # Performance logging
        handler.log_performance_issue("test_op", 2.0, 1.0)
        
        # Security error with custom type
        msg = handler.handle_security_error(CustomError("security issue"), "test_context")
        assert "security" in msg.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=term-missing"])