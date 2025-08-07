# DMPS API Reference

## Core Classes

### PromptOptimizer

Main orchestrator for prompt optimization with security and performance monitoring.

```python
from dmps import PromptOptimizer

optimizer = PromptOptimizer()
result, validation = optimizer.optimize(
    prompt_input="Your prompt here",
    mode="conversational",  # or "structured"
    platform="claude"       # claude, chatgpt, gemini, generic
)
```

**Methods:**
- `optimize(prompt_input, mode, platform)` → `(OptimizedResult, ValidationResult)`

**Security Features:**
- Automatic input validation and sanitization
- Path traversal protection for file operations
- Rate limiting and session management
- RBAC authorization for all operations

### OptimizedResult

Contains the optimization results and metadata.

```python
class OptimizedResult:
    optimized_prompt: str           # The optimized prompt
    improvements: List[str]         # Applied improvements
    methodology_applied: str        # Optimization methodology used
    metadata: Dict[str, Any]        # Performance and security metadata
    format_type: Literal['conversational', 'structured']
```

**Metadata Fields:**
- `token_metrics`: Token usage and cost estimation
- `evaluation`: Quality scores and degradation detection
- `operation_id`: Unique identifier for tracking
- `security_events`: Any security warnings or blocks

### ValidationResult

Security and input validation results.

```python
class ValidationResult:
    is_valid: bool                  # Overall validation status
    errors: List[str]               # Validation errors
    warnings: List[str]             # Security warnings
    sanitized_input: Optional[str]  # Cleaned input text
```

## Security Classes

### SecurityConfig

Central security configuration and validation.

```python
from dmps.security import SecurityConfig

# Validate file paths
if SecurityConfig.validate_file_path(filepath):
    # Safe to use file

# Check file extensions
if SecurityConfig.validate_file_extension(filename):
    # Allowed file type

# Sanitize filenames
safe_name = SecurityConfig.sanitize_filename(user_filename)
```

**Methods:**
- `validate_file_path(path)` → `bool`
- `validate_file_extension(filename)` → `bool`
- `sanitize_filename(filename)` → `str`
- `get_compiled_patterns()` → `List[Pattern]`

### AccessControl (RBAC)

Role-based access control for commands and operations.

```python
from dmps.rbac import AccessControl, Role

# Validate command access
if AccessControl.validate_command_access(Role.USER, command):
    # Command allowed

# Validate file operations
if AccessControl.validate_file_operation(Role.USER, "read", filepath):
    # File operation allowed
```

## Monitoring Classes

### ObservabilityDashboard

Performance monitoring and alerting.

```python
from dmps.observability import dashboard

# Print session summary
dashboard.print_session_summary()

# Export metrics
dashboard.export_metrics("metrics.json")

# Get performance alerts
alerts = dashboard.get_performance_alerts()
```

**Methods:**
- `print_session_summary()` → `None`
- `print_detailed_metrics()` → `None`
- `export_metrics(filepath)` → `None`
- `get_performance_alerts()` → `List[str]`

### TokenTracker

Token usage monitoring and cost estimation.

```python
from dmps.token_tracker import token_tracker

# Get session summary
summary = token_tracker.get_session_summary()

# Export trace data
token_tracker.export_traces("traces.json")

# Estimate tokens
token_count = token_tracker.estimate_tokens(text)
```

## Utility Functions

### optimize_prompt (Convenience Function)

Quick optimization without class instantiation.

```python
from dmps import optimize_prompt

result = optimize_prompt(
    "Your prompt here",
    output_mode="conversational",
    target_platform="claude"
)
```

### Input Validation

```python
from dmps.validation import InputValidator

validator = InputValidator()
result = validator.validate_input(prompt, mode)

if result.is_valid:
    # Process sanitized input
    process_prompt(result.sanitized_input)
else:
    # Handle validation errors
    for error in result.errors:
        print(f"Error: {error}")
```

## CLI Interface

### Basic Usage

```bash
# Optimize a prompt
dmps "Your prompt here" --mode conversational --platform claude

# File input/output
dmps --file input.txt --output results.txt

# Interactive mode
dmps --interactive

# REPL shell
dmps --shell
```

### Advanced Options

```bash
# Show performance metrics
dmps "Test prompt" --metrics

# Export metrics to file
dmps "Test prompt" --export-metrics metrics.json

# Quiet mode (suppress progress)
dmps "Test prompt" --quiet

# Specify platform and mode
dmps "Test prompt" --platform chatgpt --mode structured
```

## Error Handling

### Security Errors

```python
from dmps.error_handler import error_handler

try:
    result = optimizer.optimize(user_input)
except PermissionError as e:
    # Security violation
    user_msg = error_handler.handle_security_error(e, context)
    print(f"Security error: {user_msg}")
except ValueError as e:
    # Input validation error
    user_msg = error_handler.handle_error(e, context)
    print(f"Validation error: {user_msg}")
```

### Graceful Degradation

```python
# Fallback handling
fallback_value = error_handler.graceful_degradation(
    fallback_value="Default response",
    error=exception,
    context="optimization_failure"
)
```

## Configuration

### Environment Variables

```bash
# Security settings
export DMPS_MAX_INPUT_LENGTH=5000
export DMPS_MAX_FILE_SIZE=1048576
export DMPS_SESSION_TIMEOUT=1800

# Performance settings
export DMPS_CACHE_SIZE=1000
export DMPS_ENABLE_METRICS=true
```

### Programmatic Configuration

```python
from dmps.security import SecurityConfig

# Override security limits
SecurityConfig.MAX_INPUT_LENGTH = 8000
SecurityConfig.MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# Add custom validation patterns
SecurityConfig.add_dangerous_pattern(r'custom_threat_pattern')
```

## Performance Optimization

### Caching

```python
from dmps.cache import PerformanceCache

# Enable caching for better performance
cache = PerformanceCache()
cached_result = cache.get_cached_optimization(prompt_hash)
```

### Profiling

```python
from dmps.profiler import performance_monitor

@performance_monitor(threshold=0.1)
def custom_optimization_function():
    # Your optimization logic
    pass
```

## Security Best Practices

### Input Validation
- Always validate user input before processing
- Use provided sanitization functions
- Check file paths and extensions

### Error Handling
- Use secure error handlers to prevent information leakage
- Log security events for monitoring
- Implement graceful degradation

### File Operations
- Validate all file paths before operations
- Use relative paths when possible
- Restrict file extensions to safe types

### Session Management
- Implement proper session timeouts
- Monitor for suspicious activity
- Use rate limiting to prevent abuse

---

**Version**: 0.2.0  
**Last Updated**: January 7, 2025