# DMPS - Dual-Mode Prompt System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

A Python package for AI prompt optimization using the 4-D methodology (Deconstruct, Develop, Design, Deliver).

## Features

- **Intent Detection**: Automatically classifies prompt intent (creative, technical, educational, complex)
- **Gap Analysis**: Identifies missing information in prompts
- **4-D Optimization**: Applies systematic optimization techniques
- **Dual Output Modes**: Conversational and structured JSON formats
- **Platform Support**: Optimized for Claude, ChatGPT, and other AI platforms

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Using pip

```bash
pip install -e .
```

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

# Simple optimization
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

print(result.optimized_prompt)
```

### CLI Usage

```bash
python -m dmps "Your prompt here" --mode conversational --platform claude
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality

```bash
# Type checking
pyright src/

# Linting
flake8 src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
