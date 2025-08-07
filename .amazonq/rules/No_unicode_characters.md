# No Unicode Characters Rule

## Rule
Avoid using Unicode characters (emojis, special symbols) in code output and user-facing messages.

## Rationale
- Windows console encoding issues (cp1252 codec errors)
- Cross-platform compatibility
- Accessibility for all terminal environments
- Professional appearance in enterprise environments

## Examples

### ❌ Avoid
```python
print("🚀 Starting optimization...")
print("✅ Success!")
print("⚠️ Warning detected")
```

### ✅ Use Instead
```python
print("Starting optimization...")
print("Success!")
print("Warning detected")
```

## Exceptions
- Documentation files (README.md, guides) may use Unicode for visual appeal
- Internal comments may use Unicode sparingly
- Test data may include Unicode for testing purposes

## Implementation
- Use plain ASCII characters in all user-facing output
- Replace emoji indicators with descriptive text
- Use standard punctuation and symbols