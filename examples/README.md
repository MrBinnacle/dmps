# DMPS Examples

This directory contains comprehensive examples demonstrating how to use DMPS (Dual-Mode Prompt System) in various scenarios.

## Examples Overview

### 1. `basic_usage.py`
**Fundamental DMPS operations**
- Quick optimization with convenience functions
- Basic PromptOptimizer usage
- Comparing conversational vs structured modes
- Platform-specific optimization
- Intent detection examples

**Run:** `python examples/basic_usage.py`

### 2. `advanced_usage.py`
**Advanced features and patterns**
- Batch processing multiple prompts
- Using individual components for custom analysis
- Error handling and validation
- Performance analysis and metrics
- Common integration patterns

**Run:** `python examples/advanced_usage.py`

### 3. `api_integration.py`
**Integration into applications and services**
- REST API endpoint simulation
- Microservice architecture patterns
- Async/await integration
- Webhook/callback patterns
- Monitoring and metrics integration

**Run:** `python examples/api_integration.py`

## Quick Start

1. **Install DMPS:**
   ```bash
   pip install -e .
   ```

2. **Run basic examples:**
   ```bash
   python examples/basic_usage.py
   ```

3. **Try the CLI:**
   ```bash
   python -m dmps "Write a story about AI" --mode conversational
   ```

## Example Use Cases

### Content Creation
```python
from dmps import optimize_prompt

# Blog post optimization
optimized = optimize_prompt("Write about machine learning", platform="claude")
```

### Technical Documentation
```python
from dmps import PromptOptimizer

optimizer = PromptOptimizer()
result, _ = optimizer.optimize("Create API documentation", mode="structured")
```

### Educational Content
```python
# Explain complex topics
result, _ = optimizer.optimize("Explain quantum computing to beginners")
```

### Code Generation
```python
# Programming tasks
result, _ = optimizer.optimize("Write unit tests for a sorting function", platform="chatgpt")
```

## Integration Patterns

### Web API
```python
from dmps import PromptOptimizer

app = Flask(__name__)
optimizer = PromptOptimizer()

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    result, validation = optimizer.optimize(data['prompt'])
    return jsonify({"optimized": result.optimized_prompt})
```

### Batch Processing
```python
prompts = ["prompt1", "prompt2", "prompt3"]
results = [optimizer.optimize(p) for p in prompts]
```

### Async Processing
```python
import asyncio

async def async_optimize(prompt):
    return await asyncio.to_thread(optimizer.optimize, prompt)
```

## Configuration Examples

### Platform Targeting
```python
# Optimize for specific AI platforms
claude_result = optimizer.optimize(prompt, platform="claude")
chatgpt_result = optimizer.optimize(prompt, platform="chatgpt")
```

### Output Modes
```python
# Human-readable format
conv_result = optimizer.optimize(prompt, mode="conversational")

# JSON/API format
struct_result = optimizer.optimize(prompt, mode="structured")
```

## Error Handling

```python
try:
    result, validation = optimizer.optimize(user_input)
    
    if validation.is_valid:
        print(result.optimized_prompt)
    else:
        print("Validation errors:", validation.errors)
        
except Exception as e:
    print(f"Optimization failed: {e}")
```

## Performance Tips

1. **Reuse optimizer instances** - Create once, use many times
2. **Batch similar prompts** - Process related prompts together
3. **Cache results** - Store optimized prompts for repeated use
4. **Use structured mode** - For programmatic processing
5. **Handle validation** - Always check validation results

## Next Steps

- Check out the main [README.md](../README.md) for installation and setup
- Read the [API documentation](../docs/) for detailed reference
- Run the test suite: `python -m pytest tests/`
- Try the CLI: `python -m dmps --help`

## Contributing

Found an issue or want to add more examples? Please contribute!

1. Fork the repository
2. Create your example
3. Add tests if applicable
4. Submit a pull request

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/MrBinnacle/dmps/issues)
- Documentation: [Full API reference](../docs/)
- CLI Help: `python -m dmps --help`