"""
Role-Based Access Control for DMPS operations.
"""

from typing import Set, Final
from enum import Enum


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class Permission(Enum):
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EXECUTE_COMMAND = "execute_command"
    MODIFY_SETTINGS = "modify_settings"


class AccessControl:
    """RBAC implementation for DMPS"""
    
    ROLE_PERMISSIONS: Final = {
        Role.USER: {Permission.READ_FILE, Permission.EXECUTE_COMMAND, Permission.MODIFY_SETTINGS},
        Role.ADMIN: {Permission.READ_FILE, Permission.WRITE_FILE, Permission.EXECUTE_COMMAND, Permission.MODIFY_SETTINGS}
    }
    
    ALLOWED_COMMANDS: Final = frozenset({
        "help", "settings", "set", "history", "clear", "version", "save", "examples", "stats", "quit"
    })
    
    @classmethod
    def has_permission(cls, role: Role, permission: Permission) -> bool:
        """Check if role has specific permission"""
        return permission in cls.ROLE_PERMISSIONS.get(role, set())
    
    @classmethod
    def is_command_allowed(cls, command: str) -> bool:
        """Check if command is in whitelist"""
        return command in cls.ALLOWED_COMMANDS
    
    @classmethod
    def validate_file_operation(cls, role: Role, operation: str, filepath: str) -> bool:
        """Validate file operation with RBAC and path security"""
        from .security import SecurityConfig
        
        # Check path safety first
        if not SecurityConfig.is_safe_path(filepath):
            return False
        
        # Check role permissions
        if operation == "read":
            return cls.has_permission(role, Permission.READ_FILE)
        elif operation == "write":
            return cls.has_permission(role, Permission.WRITE_FILE)
        
        return False