# Security Policy

## Overview

DMPS implements comprehensive security measures to protect against common vulnerabilities and ensure safe operation.

## Security Measures Implemented

### 1. Path Traversal Protection (CWE-22)
- **File Operations**: All file read/write operations validate paths to prevent directory traversal attacks
- **Path Validation**: Centralized path validation in `SecurityConfig.is_safe_path()`
- **Blocked Patterns**: Prevents `../`, `..\\`, and absolute paths to sensitive locations

### 2. Input Validation & Sanitization
- **Length Limits**: Maximum input length of 10,000 characters
- **Line Limits**: Maximum 100 lines to prevent DoS attacks
- **Content Filtering**: Removes HTML/script tags, path traversal sequences, and code injection patterns
- **Malicious Pattern Detection**: Blocks JavaScript, eval(), exec(), and other dangerous patterns

### 3. File Operation Security
- **Size Limits**: Maximum file size of 1MB for read operations
- **Extension Validation**: Only allows `.json` and `.txt` files for save operations
- **Filename Sanitization**: Removes dangerous characters from filenames
- **Directory Creation**: Safe parent directory creation with validation

### 4. Rate Limiting & Resource Management
- **Request Limits**: Maximum 1,000 requests per REPL session
- **History Limits**: Maximum 100 items in optimization history
- **Memory Protection**: Automatic cleanup of old history items

### 5. Error Handling & Information Disclosure
- **Specific Exception Handling**: Catches specific exception types instead of generic `Exception`
- **Safe Error Messages**: Prevents internal error details from being exposed to users
- **Graceful Degradation**: Fallback mechanisms for processing failures

### 6. Regular Expression Security
- **ReDoS Protection**: Input length limits before regex processing
- **Safe Patterns**: Uses word boundaries and non-greedy matching
- **Error Handling**: Catches and handles regex errors gracefully

## Security Configuration

All security settings are centralized in `src/dmps/security.py`:

```python
class SecurityConfig:
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    MAX_INPUT_LENGTH = 10000
    MAX_LINES = 100
    MAX_REQUESTS_PER_SESSION = 1000
    MAX_HISTORY_SIZE = 100
    ALLOWED_EXTENSIONS = {'.json', '.txt'}
    BLOCKED_PATTERNS = [...]  # Malicious patterns
```

## Testing

Security measures are tested in `tests/test_security.py`:
- Path traversal attack prevention
- Malicious input detection
- File operation security
- Rate limiting functionality
- Input sanitization effectiveness

## Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do not** create a public GitHub issue
2. Email security concerns to the maintainers
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed before public disclosure

## Security Best Practices for Users

1. **File Paths**: Use relative paths within your project directory
2. **Input Validation**: Be aware that all inputs are sanitized
3. **File Extensions**: Only `.json` and `.txt` files can be saved
4. **Rate Limits**: Restart REPL sessions if you hit rate limits
5. **Updates**: Keep DMPS updated to receive security patches

## Compliance

DMPS follows security best practices including:
- OWASP Top 10 vulnerability prevention
- CWE (Common Weakness Enumeration) mitigation
- Secure coding standards
- Input validation and output encoding
- Principle of least privilege

## Security Audit History

- **2024-01**: Initial security assessment and vulnerability fixes
  - Fixed CWE-22 path traversal vulnerabilities
  - Implemented comprehensive input validation
  - Added rate limiting and resource management
  - Enhanced error handling and information disclosure protection