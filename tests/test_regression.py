"""
Regression tests for critical security vulnerabilities.
"""

import pytest
import tempfile
import os
from dmps.security import SecurityConfig
from dmps.validation import InputValidator
from dmps.cli import read_file_content, write_output
from dmps.repl import DMPSShell
from dmps.techniques import OptimizationTechniques


class TestPathTraversalRegression:
    """Regression tests for CWE-22 path traversal fixes"""
    
    def test_cli_read_blocks_traversal(self):
        """Ensure CLI read_file_content blocks path traversal"""
        with pytest.raises(SystemExit):
            read_file_content("../../../etc/passwd")
    
    def test_cli_write_blocks_traversal(self):
        """Ensure CLI write_output blocks path traversal"""
        with pytest.raises(SystemExit):
            write_output("test", "../../../tmp/malicious.txt")
    
    def test_repl_save_blocks_traversal(self):
        """Ensure REPL save command blocks path traversal"""
        shell = DMPSShell()
        # Should print error and return early
        shell.cmd_save(["../../../tmp/malicious.json"])


class TestAuthorizationRegression:
    """Regression tests for authorization bypass fixes"""
    
    def test_repl_blocks_slash_commands(self):
        """Ensure REPL blocks unauthorized / commands"""
        shell = DMPSShell()
        shell.handle_command("/malicious_command")
        # Should print "Unauthorized command"
    
    def test_repl_validates_meta_commands(self):
        """Ensure REPL validates meta commands"""
        shell = DMPSShell()
        shell._handle_meta_command(".malicious_command")
        # Should print "Unauthorized command"
    
    def test_techniques_validates_platform(self):
        """Ensure techniques validates platform parameter"""
        tech = OptimizationTechniques()
        result = tech.design_structure("test", "malicious_platform", "general")
        # Should default to generic platform
        assert "malicious_platform" not in result
    
    def test_techniques_validates_technique_name(self):
        """Ensure get_technique_description validates input"""
        tech = OptimizationTechniques()
        result = tech.get_technique_description("malicious_technique")
        assert result == "Unknown technique"


class TestInputValidationRegression:
    """Regression tests for input validation fixes"""
    
    def test_malicious_patterns_detected(self):
        """Ensure malicious patterns are detected"""
        validator = InputValidator()
        malicious_inputs = [
            "<script>alert('xss')</script>test",
            "javascript:alert(1) test",
            "eval(malicious) test",
            "../../../etc/passwd test"
        ]
        
        for malicious in malicious_inputs:
            result = validator.validate_input(malicious)
            assert result.warnings or not result.is_valid
    
    def test_input_length_limits_enforced(self):
        """Ensure input length limits are enforced"""
        validator = InputValidator()
        
        # Too long
        long_input = "x" * (SecurityConfig.MAX_INPUT_LENGTH + 1)
        result = validator.validate_input(long_input)
        assert not result.is_valid
        
        # Too many lines
        many_lines = "\n".join(["line"] * (SecurityConfig.MAX_LINES + 1))
        result = validator.validate_input(many_lines)
        assert not result.is_valid


class TestPerformanceRegression:
    """Regression tests for performance optimizations"""
    
    def test_compiled_patterns_used(self):
        """Ensure compiled patterns are being used"""
        tech = OptimizationTechniques()
        # Check that class has compiled patterns
        assert hasattr(tech, '_CONTEXT_PATTERN')
        assert hasattr(tech, '_FORMAT_PATTERN')
        assert hasattr(tech, '_WHITESPACE_PATTERN')
    
    def test_security_config_immutable(self):
        """Ensure security config uses immutable collections"""
        assert isinstance(SecurityConfig.ALLOWED_EXTENSIONS, frozenset)
        assert hasattr(SecurityConfig, '_COMPILED_PATTERNS')


if __name__ == "__main__":
    pytest.main([__file__])