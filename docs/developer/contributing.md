# Contributing to Enhanced Toolkits

Guidelines for contributing to the Enhanced Toolkits project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/malvavisc0/enhancedtoolkits.git
cd enhancedtoolkits
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## Creating New Tools

All tools must inherit from `StrictToolkit`:

```python
from enhancedtoolkits.base import StrictToolkit

class MyNewTools(StrictToolkit):
    def __init__(self):
        super().__init__()
    
    def my_function(self, param1: str, param2: int) -> dict:
        """Function description for AI agents."""
        # Implementation here
        return {"result": "success"}
```

## Code Standards

- All parameters must be required (no optional parameters)
- Include comprehensive docstrings
- Add type hints for all parameters and return values
- Follow PEP 8 style guidelines
- Include unit tests for all functions

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_reasoning.py

# Run with coverage
pytest --cov=enhancedtoolkits
```

## Documentation

Update documentation when adding new tools:

1. Add tool documentation in `docs/toolkits/`
2. Update navigation in `mkdocs.yml`
3. Add examples to relevant sections

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

## Questions?

Open an issue on GitHub for questions or discussions.