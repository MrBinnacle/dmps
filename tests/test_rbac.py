"""
Unit tests for RBAC permission boundaries.
"""

import pytest
from dmps.rbac import AccessControl, Role, Permission


class TestRBACPermissions:
    """Test role-based access control permissions"""
    
    def test_user_permissions(self):
        """Test USER role permissions"""
        assert AccessControl.has_permission(Role.USER, Permission.READ_FILE)
        assert AccessControl.has_permission(Role.USER, Permission.EXECUTE_COMMAND)
        assert AccessControl.has_permission(Role.USER, Permission.MODIFY_SETTINGS)
        assert not AccessControl.has_permission(Role.USER, Permission.WRITE_FILE)
    
    def test_admin_permissions(self):
        """Test ADMIN role permissions"""
        assert AccessControl.has_permission(Role.ADMIN, Permission.READ_FILE)
        assert AccessControl.has_permission(Role.ADMIN, Permission.WRITE_FILE)
        assert AccessControl.has_permission(Role.ADMIN, Permission.EXECUTE_COMMAND)
        assert AccessControl.has_permission(Role.ADMIN, Permission.MODIFY_SETTINGS)
    
    def test_command_whitelist(self):
        """Test command whitelist validation"""
        allowed_commands = ["help", "settings", "set", "history", "clear", "version"]
        blocked_commands = ["rm", "del", "exec", "eval", "import"]
        
        for cmd in allowed_commands:
            assert AccessControl.is_command_allowed(cmd)
        
        for cmd in blocked_commands:
            assert not AccessControl.is_command_allowed(cmd)
    
    def test_file_operation_validation(self):
        """Test file operation validation with RBAC"""
        # Safe file paths
        safe_files = ["test.txt", "output.json", "data/file.txt"]
        
        for filepath in safe_files:
            assert AccessControl.validate_file_operation(Role.USER, "read", filepath)
            assert not AccessControl.validate_file_operation(Role.USER, "write", filepath)
            assert AccessControl.validate_file_operation(Role.ADMIN, "write", filepath)
        
        # Dangerous file paths
        dangerous_files = ["../../../etc/passwd", "/root/.ssh/id_rsa", "C:\\Windows\\System32\\config\\SAM"]
        
        for filepath in dangerous_files:
            assert not AccessControl.validate_file_operation(Role.USER, "read", filepath)
            assert not AccessControl.validate_file_operation(Role.ADMIN, "write", filepath)


if __name__ == "__main__":
    pytest.main([__file__])