# Optional Dependencies Rule

## Rule
Use `TYPE_CHECKING` pattern for optional dependencies instead of `# type: ignore` comments.

## Rationale
- Cleaner code without suppression comments
- Proper type hints during development
- Graceful runtime fallbacks
- Standard Python pattern for optional imports

## Pattern

### ✅ Correct
```python
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from transformers import pipeline
    import requests

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None
```

### ❌ Avoid
```python
try:
    from transformers import pipeline  # type: ignore
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None  # type: ignore
```

## Implementation
- Import under `TYPE_CHECKING` for type hints
- Use try/except for runtime availability
- Set to `None` on import failure
- Check availability flags before usage
- Provide fallback behavior

## Benefits
- IDE gets proper type information
- No type checker warnings
- Clean, readable code
- Follows Python best practices
