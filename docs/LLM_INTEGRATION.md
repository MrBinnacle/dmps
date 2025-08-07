# LLM Integration Guide

## Overview

DMPS includes built-in LLM API routing with LangChain integration for production-ready prompt optimization.

## Installation

### Basic Installation (Mock Mode)
```bash
pip install dmps
```

### With LLM Support
```bash
pip install dmps[llm]
```

## Configuration

### Environment Variables
```bash
# OpenAI
export OPENAI_API_KEY="your-openai-key"

# Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### Usage Examples

#### Basic Usage (Auto-detects API keys)
```python
from dmps import optimize_prompt

# Uses Claude if ANTHROPIC_API_KEY is set
result = optimize_prompt("Write a story about AI", platform="claude")

# Uses GPT if OPENAI_API_KEY is set
result = optimize_prompt("Debug this code", platform="chatgpt")
```

#### Advanced Configuration
```python
from dmps.llm_client import LLMRouter, OpenAIClient, AnthropicClient

# Custom router with specific models
router = LLMRouter()
router.clients["openai"] = OpenAIClient(model="gpt-4")
router.clients["anthropic"] = AnthropicClient(model="claude-3-opus-20240229")

response = router.generate("Optimize this prompt", platform="claude")
```

## Supported Platforms

| Platform | LLM Provider | Model | Fallback |
|----------|--------------|-------|----------|
| `claude` | Anthropic | claude-3-sonnet | Mock |
| `chatgpt` | OpenAI | gpt-3.5-turbo | Mock |
| `generic` | Mock | mock-model | N/A |
| `gemini` | Mock* | mock-model | N/A |

*Google Gemini integration planned for future release

## Features

### Automatic Fallback
- Falls back to mock optimization if API keys missing
- Graceful error handling for API failures
- No interruption to user workflow

### Cost Tracking
- Real-time token usage estimation
- Cost calculation per request
- Usage analytics and reporting

### Performance Optimization
- Lazy-loaded clients for faster startup
- Connection pooling and retry logic
- Caching for repeated requests

## Development Roadmap

### v0.3.0 (Next Release)
- [ ] Google Gemini integration
- [ ] Azure OpenAI support
- [ ] Custom model fine-tuning
- [ ] Batch processing API

### v0.4.0 (Future)
- [ ] Local model support (Ollama)
- [ ] Multi-model ensemble optimization
- [ ] A/B testing framework
- [ ] Advanced prompt templates

## Troubleshooting

### Common Issues

**No API Response**
```python
# Check if LangChain is installed
from dmps.llm_client import LANGCHAIN_AVAILABLE
print(f"LangChain available: {LANGCHAIN_AVAILABLE}")
```

**API Key Issues**
```python
import os
print(f"OpenAI key set: {'OPENAI_API_KEY' in os.environ}")
print(f"Anthropic key set: {'ANTHROPIC_API_KEY' in os.environ}")
```

**Mock Fallback Mode**
- DMPS automatically uses mock optimization when API keys are missing
- This ensures the package works out-of-the-box for testing
- Mock responses include realistic optimization patterns

## Security

- API keys are never logged or exposed
- All requests use secure HTTPS connections
- Input sanitization prevents prompt injection
- Rate limiting prevents API abuse
