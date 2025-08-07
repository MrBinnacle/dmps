# DMPS - Dual-Mode Prompt System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/dmps.svg)](https://pypi.org/project/dmps/)
[![Security](https://img.shields.io/badge/security-hardened-green.svg)](https://github.com/MrBinnacle/dmps/blob/main/docs/SECURITY_GUIDE.md)

A secure, enterprise-grade Python package for AI prompt optimization using the 4-D methodology (Deconstruct, Develop, Design, Deliver).

## Features

### Core Optimization
- **Intent Detection**: Automatically classifies prompt intent (creative, technical, educational, analytical)
- **Gap Analysis**: Identifies missing information and optimization opportunities
- **4-D Optimization**: Systematic optimization using proven methodologies
- **Dual Output Modes**: Conversational and structured JSON formats
- **Platform Support**: Optimized for Claude, ChatGPT, Gemini, and generic platforms

### Security & Performance (v0.2.0)
- **Enterprise Security**: Path traversal protection, RBAC, input sanitization
- **Token Tracking**: Cost estimation and usage monitoring
- **Context Engineering**: Performance evaluation and optimization metrics
- **Observability**: Real-time monitoring and alerting dashboard
- **Code Quality**: Pre-commit hooks, automated testing, type safety

## Installation

### From PyPI (Recommended)

```bash
pip install dmps==0.2.0
```

### From Source

```bash
# Clone the repository
git clone https://github.com/MrBinnacle/dmps.git
cd dmps

# Install in development mode
pip install -e .
```

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Development Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MrBinnacle/dmps.git
   cd dmps
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Quick Start

```python
from dmps import optimize_prompt

# Simple optimization with automatic security validation
result = optimize_prompt("Write a story about AI")
print(result)
```

### Advanced Usage

```python
from dmps import PromptOptimizer

optimizer = PromptOptimizer()
result, validation = optimizer.optimize(
    "Explain machine learning",
    mode="conversational",
    platform="claude"
)

# Check for security warnings
if validation.warnings:
    print("Security warnings:", validation.warnings)

# Access optimization metadata
print(f"Token reduction: {result.metadata['token_metrics']['token_reduction']}")
print(f"Quality score: {result.metadata['evaluation']['overall_score']}")
print(result.optimized_prompt)
```

### Token Tracking & Observability

```python
from dmps.observability import dashboard
from dmps.token_tracker import token_tracker

# Monitor performance
dashboard.print_session_summary()

# Export metrics
dashboard.export_metrics("metrics.json")

# Get performance alerts
alerts = dashboard.get_performance_alerts()
for alert in alerts:
    print(f"Alert: {alert}")
```

## 🛡️ Enterprise Security (v0.2.0)

DMPS includes comprehensive security protections:

- **CWE-22 Protection**: Path traversal attack prevention
- **Input Sanitization**: XSS and code injection prevention  
- **RBAC Authorization**: Role-based access control for all operations
- **Rate Limiting**: Protection against abuse and DoS attacks
- **Secure Error Handling**: Information leak prevention
- **Audit Logging**: Complete security event tracking
- **Token Validation**: Secure API token management

**Security Compliance**: Follows OWASP guidelines and enterprise security standards.

### CLI Usage

```bash
# Basic usage with automatic security validation
dmps "Your prompt here" --mode conversational --platform claude

# File input/output (automatically validates paths)
dmps --file input.txt --output results.txt

# Interactive mode with security monitoring
dmps --interactive

# REPL shell mode with RBAC protection
dmps --shell

# Show performance metrics
dmps "Optimize this" --metrics

# Export metrics to file
dmps "Test prompt" --export-metrics metrics.json

# Help
dmps --help
```

**Security Features:**
- Automatic path traversal protection
- Input sanitization and validation
- RBAC-controlled command access
- Rate limiting and session management
- Secure file operations with extension validation

## Development

### Setup Development Environment

```bash
# Install development tools and pre-commit hooks
python setup-dev.py

# Run quality checks
python scripts/format.py
```

### Running Tests

```bash
python -m pytest tests/ -v
```

### Code Quality

```bash
# Automated formatting and linting
black src/
isort src/
flake8 src/
mypy src/

# Security scanning
bandit -r src/
safety check
```

### Quality Guardrails

- **Pre-commit hooks**: Automatic code quality validation
- **CI/CD pipeline**: Automated testing and security scanning  
- **Type checking**: Full mypy integration
- **Security scanning**: Bandit and safety checks

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete guidelines.

## What's New in v0.2.0

- **Enterprise Security**: Complete security hardening with CWE-22 protection
- **Token Tracking**: Cost estimation and usage monitoring
- **Observability Dashboard**: Real-time performance monitoring
- **Code Quality Guardrails**: Pre-commit hooks and automated validation
- **Enhanced Performance**: 3-5x improvement in pattern matching
- **Type Safety**: Full mypy integration and type annotations

See [CHANGELOG.md](CHANGELOG.md) for complete release notes.

## Contributing

Contributions are welcome! Please read [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Run quality checks: `python scripts/format.py`
4. Submit a Pull Request

All contributions must pass security and quality checks.

## Links

- **PyPI**: https://pypi.org/project/dmps/
- **GitHub**: https://github.com/MrBinnacle/dmps
- **Documentation**: [docs/](docs/)
- **Security Guide**: [docs/SECURITY_GUIDE.md](docs/SECURITY_GUIDE.md)
- **Development Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**DMPS v0.2.0** - Enterprise-grade AI prompt optimization with comprehensive security and observability.
