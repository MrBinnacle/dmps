# Development Guidelines

## Code Quality Standards

### Automated Enforcement
- **Pre-commit hooks** prevent bad code from being committed
- **CI/CD pipeline** blocks merges with quality issues
- **IDE integration** provides real-time feedback

### Setup Development Environment
```bash
python setup-dev.py
```

### Daily Workflow
```bash
# Before coding
git pull origin main

# During development - automatic formatting on save in IDE

# Before committing
python scripts/format.py

# Commit (pre-commit hooks run automatically)
git commit -m "feat: your changes"
```

### Code Standards
- **Line length**: 88 characters max
- **Formatting**: Black (automatic)
- **Import sorting**: isort (automatic)
- **Linting**: Ruff (zero violations)
- **Type hints**: mypy (basic checking)

### Security Standards
- **No hardcoded secrets**
- **Path traversal protection**
- **Input validation required**
- **Error handling must not leak info**

### Violation Prevention
1. **IDE warns in real-time**
2. **Pre-commit blocks bad commits**
3. **CI/CD blocks bad merges**
4. **Code review catches edge cases**

### Quick Fixes
```bash
# Fix formatting
black src/

# Fix imports
isort src/

# Check issues
ruff check src/
```
