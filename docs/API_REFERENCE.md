# DMPS API Reference

## Core Functions

### `optimize_prompt(user_prompt, output_mode, target_platform)`
Quick optimization function with built-in security validation.

**Parameters:**
- `user_prompt` (str): Input prompt to optimize (automatically sanitized)
- `output_mode` (str): "conversational" or "structured" 
- `target_platform` (str): "claude", "chatgpt", "gemini", or "generic"

**Returns:**
- `str`: Optimized prompt

**Security Features:**
- Automatic input sanitization
- Length and content validation
- Malicious pattern detection

```python
from dmps import optimize_prompt

# Secure optimization with validation
result = optimize_prompt("Write a story about AI", "conversational", "claude")
```

## Classes

### `PromptOptimizer`
Main orchestrator with comprehensive security controls.

#### `optimize(user_prompt, output_mode, target_platform)`
**Returns:** `(OptimizedResult, ValidationResult)`

```python
from dmps import PromptOptimizer

optimizer = PromptOptimizer()
result, validation = optimizer.optimize("Your prompt", "conversational", "claude")

# Check security warnings
if validation.warnings:
    print("Security issues detected:", validation.warnings)
```

### `SecurityConfig`
Centralized security configuration and validation.

#### `is_safe_path(filepath)`
Validates file paths against traversal attacks.

```python
from dmps.security import SecurityConfig

# Path validation
if SecurityConfig.is_safe_path("user_file.txt"):
    # Safe to proceed
    pass
```

#### `validate_multiple_paths(filepaths)`
Batch validate multiple file paths for performance.

### `InputValidator`
Comprehensive input validation and sanitization.

#### `validate_input(prompt_input, mode)`
**Returns:** `ValidationResult`

```python
from dmps.validation import InputValidator

validator = InputValidator()
result = validator.validate_input("<script>alert('xss')</script>Write a story")

print("Valid:", result.is_valid)
print("Warnings:", result.warnings)  # XSS detected
print("Sanitized:", result.sanitized_input)  # Script tags removed
```

### `AccessControl` (RBAC)
Role-based access control system.

#### `validate_file_operation(role, operation, filepath)`
Validates file operations with RBAC and path security.

```python
from dmps.rbac import AccessControl, Role

# Check if user can read file
if AccessControl.validate_file_operation(Role.USER, "read", "data.txt"):
    # Operation allowed
    pass
```

## Security Classes

### `SecureErrorHandler`
Secure error handling with information leak prevention.

```python
from dmps.error_handler import error_handler

try:
    # Some operation
    pass
except Exception as e:
    safe_message = error_handler.handle_error(e, "operation_context")
    print(safe_message)  # No sensitive information leaked
```

### `PerformanceCache`
LRU caching with security considerations.

```python
from dmps.cache import PerformanceCache

# Cached operations for performance
prompt_hash = PerformanceCache.get_prompt_hash("user prompt")
intent = PerformanceCache.cached_intent_classification(prompt_hash, "user prompt")
```

## Data Structures

### `ValidationResult`
Result of input validation with security information.

```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]  # Security warnings
    sanitized_input: Optional[str]
```

### `OptimizedResult`
Result of prompt optimization.

```python
@dataclass
class OptimizedResult:
    optimized_prompt: str
    improvements: List[str]
    methodology_applied: str
    metadata: Dict[str, Any]
    format_type: Literal['conversational', 'structured']
```

## Security Constants

### File Operation Limits
```python
SecurityConfig.MAX_FILE_SIZE = 1024 * 1024  # 1MB
SecurityConfig.MAX_INPUT_LENGTH = 10000
SecurityConfig.MAX_LINES = 100
```

### Rate Limiting
```python
SecurityConfig.MAX_REQUESTS_PER_SESSION = 1000
SecurityConfig.MAX_HISTORY_SIZE = 100
```

### Allowed Extensions
```python
SecurityConfig.ALLOWED_EXTENSIONS = {'.json', '.txt'}
```

## Error Handling

All DMPS functions use secure error handling:

```python
try:
    result = optimize_prompt("user input")
except Exception as e:
    # Errors are automatically handled securely
    # No sensitive information is exposed
    pass
```

## Performance Monitoring

DMPS includes automatic performance monitoring:

```python
from dmps.profiler import performance_monitor

@performance_monitor(threshold=0.1)
def my_function():
    # Function is automatically monitored
    # Slow operations are logged
    pass
```

## Thread Safety

DMPS components are designed to be thread-safe:
- Compiled regex patterns are immutable
- Caching uses thread-safe LRU cache
- Error handling is stateless

## Best Practices

1. **Always check validation results** for security warnings
2. **Use relative file paths** within your project directory
3. **Monitor logs** for security events
4. **Handle ValidationResult.warnings** in production code
5. **Use RBAC validation** for file operations

## Migration Guide

### From v0.0.x to v0.1.0
- All functions now include automatic security validation
- File operations require path validation
- Input sanitization is automatic
- Error messages are now secure (no information leakage)

```python
# Old (insecure)
result = old_optimize("user input")

# New (secure)
result = optimize_prompt("user input")  # Automatic validation
```