# DMPS Security Guide

## 🛡️ Security Features Overview

DMPS implements comprehensive security measures to protect against common vulnerabilities and ensure safe operation.

## 🔒 Built-in Security Protections

### Path Traversal Protection (CWE-22)
DMPS automatically blocks dangerous file paths:

```python
# ❌ These are automatically blocked
dmps --file "../../../etc/passwd"
dmps --output "/root/.ssh/id_rsa"

# ✅ These are safe and allowed
dmps --file "my_prompts.txt"
dmps --output "results/output.json"
```

**What's Protected:**
- Directory traversal attempts (`../`, `..\\`)
- Access to system directories (`/etc/`, `C:\Windows`)
- Absolute paths outside project directory

### Input Validation & Sanitization
All user input is automatically validated and sanitized:

```python
from dmps import optimize_prompt

# Malicious input is automatically detected and sanitized
result = optimize_prompt("<script>alert('xss')</script>Write a story")
# Script tags are removed, warnings are generated
```

**Protected Against:**
- XSS attacks (script injection)
- Code injection (eval, exec, __import__)
- Path traversal in prompts
- Excessive input length (DoS prevention)

### Role-Based Access Control (RBAC)
Commands are restricted based on user roles:

```python
# USER role permissions:
# ✅ Read files, execute commands, modify settings
# ❌ Write files (admin only)

# Only whitelisted commands are allowed:
# ✅ help, settings, set, history, clear, version
# ❌ rm, del, exec, eval, import
```

## 🚨 Security Monitoring

### Automatic Threat Detection
DMPS continuously monitors for security threats:

```bash
# Security events are logged automatically
tail -f dmps_errors.log | grep SECURITY
```

### Rate Limiting
Built-in protection against abuse:
- Maximum 1,000 requests per REPL session
- Maximum 100 items in history
- Automatic cleanup of old data

## 🔧 Security Configuration

### File Operation Limits
```python
# Configurable security limits
MAX_FILE_SIZE = 1MB        # Maximum file size for reading
MAX_INPUT_LENGTH = 10,000  # Maximum prompt length
MAX_LINES = 100           # Maximum lines in input
```

### Allowed File Extensions
Only safe file types are permitted for save operations:
```python
ALLOWED_EXTENSIONS = {'.json', '.txt'}  # Only these extensions allowed
```

## 📋 Security Best Practices

### For Users
1. **Use Relative Paths**: Always use paths within your project directory
2. **Validate Input**: Be aware that all inputs are automatically sanitized
3. **Monitor Logs**: Check `dmps_errors.log` for security events
4. **Update Regularly**: Keep DMPS updated for latest security patches

### For Developers
1. **Input Validation**: All user inputs go through `InputValidator`
2. **Path Checking**: Use `SecurityConfig.is_safe_path()` for file operations
3. **Error Handling**: Use `SecureErrorHandler` to prevent information leaks
4. **RBAC**: Check permissions with `AccessControl.validate_file_operation()`

## 🔍 Security Testing

### Manual Security Tests
```bash
# Test path traversal protection
python -c "from dmps.security import SecurityConfig; print('Protected:', not SecurityConfig.is_safe_path('../../../etc/passwd'))"

# Test XSS detection
python -c "from dmps.validation import InputValidator; v = InputValidator(); r = v.validate_input('<script>alert(1)</script>'); print('Detected:', bool(r.warnings))"
```

### Automated Security Scans
DMPS includes automated security scanning:
- **Bandit**: Static security analysis
- **Safety**: Dependency vulnerability scanning
- **Semgrep**: Advanced security pattern detection

## 🚨 Incident Response

### If You Suspect a Security Issue
1. **Stop using the affected feature immediately**
2. **Check logs**: `dmps_errors.log` for security events
3. **Report the issue**: Create a GitHub issue with details
4. **Update DMPS**: Ensure you're using the latest version

### Security Event Types
- `SECURITY VIOLATION`: Blocked malicious input
- `Path traversal blocked`: Dangerous file path detected
- `Access denied`: RBAC permission violation
- `Rate limit exceeded`: Too many requests detected

## 📞 Security Contact

For security vulnerabilities:
- **Email**: security@dmps-project.com
- **GitHub**: Create a private security advisory
- **Response Time**: 24-48 hours for critical issues

## 🔄 Security Updates

DMPS automatically checks for security updates:
- Daily security scans via CI/CD
- Automatic dependency vulnerability checks
- Regular security audits and penetration testing

Stay secure with DMPS! 🛡️