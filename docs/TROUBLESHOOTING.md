# DMPS Troubleshooting Guide

## 🚨 Security-Related Issues

### Path Access Denied
**Error:** `Security validation failed` or `Invalid file path`

**Cause:** DMPS blocked a potentially dangerous file path.

**Solution:**
```bash
# ❌ Blocked paths
dmps --file "../../../etc/passwd"
dmps --output "/root/sensitive.txt"

# ✅ Safe paths
dmps --file "my_prompts.txt"
dmps --output "results/output.json"
```

### Input Validation Warnings
**Warning:** `Input contains potentially problematic content`

**Cause:** Malicious patterns detected in input.

**Solution:**
```python
from dmps.validation import InputValidator

validator = InputValidator()
result = validator.validate_input("your input")

if result.warnings:
    print("Issues found:", result.warnings)
    print("Sanitized input:", result.sanitized_input)
```

### Rate Limit Exceeded
**Error:** `Rate limit exceeded. Please restart the session.`

**Cause:** Too many requests in REPL session (>1000).

**Solution:**
- Restart the REPL session
- Use CLI mode for batch processing
- Implement delays between requests

### Access Denied Commands
**Error:** `Access denied: /command` or `Unauthorized command`

**Cause:** RBAC blocked unauthorized command.

**Solution:**
```python
# ✅ Allowed commands
.help, .settings, .set, .history, .clear, .version

# ❌ Blocked commands  
/rm, /del, /exec, /eval
```

## 🔧 Performance Issues

### Slow Optimization
**Issue:** Optimization takes too long

**Diagnosis:**
```python
# Check performance logs
tail -f dmps_errors.log | grep "Performance issue"
```

**Solutions:**
- Use shorter prompts (< 1000 characters)
- Enable caching for repeated operations
- Check system resources

### Memory Usage
**Issue:** High memory consumption

**Solutions:**
- Clear REPL history: `.clear`
- Restart REPL sessions periodically
- Use CLI mode for large batches

## 📁 File Operation Issues

### File Not Found
**Error:** `File not found. Check the file path and ensure it exists.`

**Solutions:**
1. Verify file exists: `ls -la filename.txt`
2. Use absolute paths within project directory
3. Check file permissions

### File Too Large
**Error:** `File too large: filename.txt`

**Cause:** File exceeds 1MB limit.

**Solutions:**
- Split large files into smaller chunks
- Use streaming for large inputs
- Increase limit in configuration (advanced)

### Invalid File Extension
**Error:** `Only .json and .txt files are allowed`

**Cause:** Trying to save to unsupported file type.

**Solutions:**
```bash
# ✅ Supported extensions
dmps --output results.txt
dmps --output data.json

# ❌ Blocked extensions
dmps --output script.py
dmps --output config.exe
```

## 🐛 Common Errors

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'dmps'`

**Solutions:**
```bash
# Reinstall DMPS
pip uninstall dmps
pip install dmps

# Or install in development mode
pip install -e .
```

### Type Errors
**Error:** `TypeError: expected str, got NoneType`

**Cause:** Passing None or invalid types.

**Solution:**
```python
# ✅ Correct usage
result = optimize_prompt("valid string input")

# ❌ Invalid usage
result = optimize_prompt(None)
result = optimize_prompt(123)
```

### Validation Errors
**Error:** `Input too short (minimum 5 characters)`

**Solutions:**
- Ensure input has at least 5 characters
- Check for empty strings or whitespace-only input

## 🔍 Debugging Steps

### 1. Check Logs
```bash
# View error logs
tail -f dmps_errors.log

# Filter security events
grep "SECURITY" dmps_errors.log

# Filter performance issues
grep "Performance issue" dmps_errors.log
```

### 2. Validate Input
```python
from dmps.validation import InputValidator

validator = InputValidator()
result = validator.validate_input("your problematic input")

print("Valid:", result.is_valid)
print("Errors:", result.errors)
print("Warnings:", result.warnings)
```

### 3. Test Security
```python
from dmps.security import SecurityConfig

# Test path safety
print("Safe path:", SecurityConfig.is_safe_path("your/file/path"))

# Test multiple paths
paths = ["file1.txt", "../file2.txt", "folder/file3.txt"]
results = SecurityConfig.validate_multiple_paths(paths)
print("Path results:", results)
```

### 4. Check Performance
```python
from dmps.profiler import performance_tracker

# View slow operations
slow_ops = performance_tracker.get_slow_operations(threshold=0.1)
print("Slow operations:", slow_ops)
```

## 🆘 Getting Help

### Before Reporting Issues
1. **Check logs**: `dmps_errors.log` for detailed error information
2. **Test with minimal input**: Isolate the problem
3. **Verify installation**: `pip show dmps`
4. **Check Python version**: Python 3.8+ required

### Reporting Security Issues
**🚨 IMPORTANT:** Report security vulnerabilities privately

1. **Email**: security@dmps-project.com
2. **GitHub**: Create private security advisory
3. **Include**: Steps to reproduce, expected vs actual behavior

### Reporting Bugs
Create GitHub issue with:
- DMPS version: `pip show dmps`
- Python version: `python --version`
- Operating system
- Complete error message
- Minimal reproduction code

### Performance Issues
Include in your report:
- Input size and complexity
- System specifications
- Performance logs from `dmps_errors.log`
- Expected vs actual performance

## 🔄 Recovery Procedures

### Reset REPL Session
```python
# Clear all data and restart
shell = DMPSShell()
shell._clear_history()
shell.request_count = 0
```

### Clear Cache
```python
# Clear performance cache
from dmps.cache import PerformanceCache
# Cache automatically manages size, but restart Python to clear
```

### Reset Configuration
```bash
# Remove configuration files
rm -f ~/.dmps/config.json
rm -f dmps_errors.log

# Reinstall clean
pip uninstall dmps
pip install dmps
```

## 📞 Support Channels

- **Documentation**: [docs/](docs/)
- **GitHub Issues**: Bug reports and feature requests
- **Security**: security@dmps-project.com
- **Community**: GitHub Discussions

Remember: DMPS prioritizes security and will block potentially dangerous operations. This is by design to keep your system safe! 🛡️