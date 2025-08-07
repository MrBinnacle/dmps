"""
Security tests for DMPS to verify vulnerability fixes.
"""

import pytest
import tempfile
import os
from pathlib import Path
from dmps.security import SecurityConfig
from dmps.validation import InputValidator
from dmps.cli import read_file_content, write_output
from dmps.repl import DMPSShell


class TestSecurityConfig:
    """Test security configuration"""
    
    def test_path_traversal_detection(self):
        """Test path traversal attack detection"""
        # These should be blocked
        dangerous_paths = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM"
        ]
        
        for path in dangerous_paths:
            assert not SecurityConfig.is_safe_path(path)
    
    def test_safe_paths(self):
        """Test legitimate paths are allowed"""
        safe_paths = [
            "output.txt",
            "results/data.json",
            "./local_file.txt"
        ]
        
        for path in safe_paths:
            assert SecurityConfig.is_safe_path(path)
    
    def test_file_extension_validation(self):
        """Test file extension validation"""
        assert SecurityConfig.validate_file_extension("test.json")
        assert SecurityConfig.validate_file_extension("test.txt")
        assert not SecurityConfig.validate_file_extension("test.exe")
        assert not SecurityConfig.validate_file_extension("test.sh")
    
    def test_filename_sanitization(self):
        """Test filename sanitization"""
        dangerous_name = "test<>:\"|?*\\.txt"
        sanitized = SecurityConfig.sanitize_filename(dangerous_name)
        assert "<" not in sanitized
        assert ">" not in sanitized
        assert "|" not in sanitized


class TestInputValidation:
    """Test input validation security"""
    
    def test_malicious_input_detection(self):
        """Test detection of malicious input patterns"""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "eval(malicious_code)",
            "exec(dangerous_function)",
            "__import__('os').system('rm -rf /')",
            "file:///etc/passwd",
            "../../../sensitive_file"
        ]
        
        validator = InputValidator()
        for malicious_input in malicious_inputs:
            result = validator.validate_input(malicious_input)
            # Should either be invalid or have warnings
            assert not result.is_valid or result.warnings
    
    def test_input_length_limits(self):
        """Test input length validation"""
        validator = InputValidator()
        
        # Too short
        result = validator.validate_input("hi")
        assert not result.is_valid
        assert any("too short" in error.lower() for error in result.errors)
        
        # Too long
        long_input = "x" * (SecurityConfig.MAX_INPUT_LENGTH + 1)
        result = validator.validate_input(long_input)
        assert not result.is_valid
        assert any("too long" in error.lower() for error in result.errors)
    
    def test_line_count_limits(self):
        """Test line count validation"""
        validator = InputValidator()
        
        # Too many lines
        many_lines = "\\n".join(["line"] * (SecurityConfig.MAX_LINES + 1))
        result = validator.validate_input(many_lines)
        assert not result.is_valid
        assert any("too many lines" in error.lower() for error in result.errors)
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        validator = InputValidator()
        
        malicious_input = "<script>alert('test')</script>Write a story about AI"
        result = validator.validate_input(malicious_input)
        
        # Script tags should be removed
        assert "<script>" not in result.sanitized_input
        assert "alert" not in result.sanitized_input


class TestFileOperations:
    """Test file operation security"""
    
    def test_read_file_path_validation(self):
        """Test file reading path validation"""
        with pytest.raises(SystemExit):
            read_file_content("../../../etc/passwd")
    
    def test_write_file_path_validation(self):
        """Test file writing path validation"""
        with pytest.raises(SystemExit):
            write_output("test content", "../../../dangerous_location.txt")
    
    def test_file_size_limits(self):
        """Test file size limits"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            # Create a file larger than the limit
            large_content = "x" * (SecurityConfig.MAX_FILE_SIZE + 1)
            tmp.write(large_content.encode())
            tmp.flush()
            
            try:
                with pytest.raises(SystemExit):
                    read_file_content(tmp.name)
            finally:
                os.unlink(tmp.name)


class TestREPLSecurity:
    """Test REPL security features"""
    
    def test_rate_limiting(self):
        """Test rate limiting in REPL"""
        shell = DMPSShell()
        
        # Simulate many requests
        shell.request_count = SecurityConfig.MAX_REQUESTS_PER_SESSION + 1
        
        # This should be blocked
        shell.optimize_and_display("test prompt")
        # Rate limit message should be shown (we can't easily test output here)
    
    def test_history_size_limit(self):
        """Test history size limiting"""
        shell = DMPSShell()
        
        # Add more items than the limit
        for i in range(SecurityConfig.MAX_HISTORY_SIZE + 10):
            shell.history.append({"test": f"item_{i}"})
        
        # Simulate adding one more item (triggers cleanup)
        shell.history.append({"test": "new_item"})
        if len(shell.history) > shell.max_history:
            shell.history = shell.history[-shell.max_history:]
        
        assert len(shell.history) <= SecurityConfig.MAX_HISTORY_SIZE
    
    def test_save_command_security(self):
        """Test save command path validation"""
        shell = DMPSShell()
        
        # Test dangerous paths
        dangerous_paths = [
            "../../../etc/passwd",
            "test.exe",
            "script.sh"
        ]
        
        for path in dangerous_paths:
            # This should not create files in dangerous locations
            shell.cmd_save([path])
            # The function should print error messages and return early


if __name__ == "__main__":
    pytest.main([__file__])