# Developer Guide

Welcome to the Enhanced Toolkits developer guide! This section provides information for developers who want to contribute to the project, understand the codebase, or deploy their own instances.

## 🚀 Quick Start for Developers

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/malvavisc0/enhancedtoolkits.git
   cd enhancedtoolkits
   ```

2. **Create development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests**:
   ```bash
   pytest
   ```

## 📁 Project Structure

```
enhancedtoolkits/
├── src/enhancedtoolkits/          # Main package
│   ├── __init__.py                # Package initialization
│   ├── base.py                    # StrictToolkit base class
│   ├── reasoning.py               # Reasoning tools
│   ├── searxng.py                 # Search tools
│   ├── thinking.py                # Thinking tools
│   ├── files.py                   # File operations
│   ├── finance.py                 # Financial data
│   ├── youtube.py                 # YouTube integration
│   ├── weather.py                 # Weather data
│   ├── downloader.py              # Content downloading
│   ├── calculators/               # Calculator modules
│   │   ├── __init__.py
│   │   ├── base.py                # Calculator base classes
│   │   ├── arithmetic.py          # Basic math operations
│   │   ├── time_value.py          # Time value of money
│   │   ├── investment.py          # Investment analysis
│   │   ├── loan.py                # Loan calculations
│   │   ├── bond.py                # Bond valuations
│   │   ├── risk.py                # Risk metrics
│   │   ├── depreciation.py        # Asset depreciation
│   │   ├── business.py            # Business analysis
│   │   └── utility.py             # Utility functions
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       └── schema.py              # Data schemas
├── docs/                          # Documentation
├── tests/                         # Test suite
├── pyproject.toml                 # Project configuration
├── README.md                      # Project overview
└── LICENSE                        # MIT License
```

## 🏗️ Architecture Overview

### StrictToolkit Base Class

All toolkits inherit from `StrictToolkit`, which provides:

- **Parameter validation**: Ensures all parameters are marked as required
- **OpenAI compatibility**: Consistent function calling interface
- **Error handling**: Standardized error responses
- **Logging**: Comprehensive logging and debugging

```python
from enhancedtoolkits.base import StrictToolkit

class MyCustomToolkit(StrictToolkit):
    def my_method(self, required_param: str, optional_param: str = "default") -> str:
        """All parameters become required in the JSON schema."""
        return f"Result: {required_param}, {optional_param}"
```

### Toolkit Design Patterns

#### 1. Input Validation
```python
def _validate_inputs(self, **kwargs):
    """Validate all input parameters."""
    for key, value in kwargs.items():
        if not isinstance(value, expected_type):
            raise ValueError(f"Invalid {key}: {value}")
```

#### 2. Error Handling
```python
try:
    result = self._perform_operation()
    return self._format_success_response(result)
except SpecificError as e:
    return self._format_error_response("operation", str(e))
```

#### 3. Caching
```python
@lru_cache(maxsize=128)
def _cached_operation(self, cache_key: str):
    """Cache expensive operations."""
    return self._expensive_operation(cache_key)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=enhancedtoolkits

# Run specific test file
pytest tests/test_reasoning.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py                    # Test configuration
├── test_base.py                   # Base class tests
├── test_reasoning.py              # Reasoning tools tests
├── test_finance.py                # Finance tools tests
├── test_calculators/              # Calculator tests
│   ├── test_arithmetic.py
│   ├── test_time_value.py
│   └── ...
└── integration/                   # Integration tests
    ├── test_toolkit_integration.py
    └── test_api_compatibility.py
```

### Writing Tests

```python
import pytest
from enhancedtoolkits import CalculatorTools

class TestArithmeticCalculator:
    def setup_method(self):
        self.calculator = CalculatorTools()
    
    def test_add_positive_numbers(self):
        result = self.calculator.add(5, 3)
        assert result == "8"
    
    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ZeroDivisionError):
            self.calculator.divide(10, 0)
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, "2"),
        (0, 5, "5"),
        (-3, 3, "0")
    ])
    def test_add_various_inputs(self, a, b, expected):
        result = self.calculator.add(a, b)
        assert result == expected
```

## 🔧 Development Tools

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Code formatting
black src/ tests/

# Import sorting
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run quality checks:

```bash
pip install pre-commit
pre-commit install
```

### Configuration Files

- **`pyproject.toml`**: Project metadata and tool configuration
- **`.github/workflows/`**: CI/CD pipeline configuration
- **`pytest.ini`**: Test configuration
- **`.gitignore`**: Git ignore patterns

## 📦 Building and Distribution

### Building the Package

```bash
# Install build tools
pip install build

# Build the package
python -m build

# This creates:
# dist/enhancedtoolkits-x.x.x-py3-none-any.whl
# dist/enhancedtoolkits-x.x.x.tar.gz
```

### Local Installation

```bash
# Install in development mode
pip install -e .

# Install with all dependencies
pip install -e ".[full]"
```

## 🚀 Deployment

### Documentation Deployment

```bash
# Install MkDocs dependencies
pip install -r docs/requirements.txt

# Serve documentation locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Release Process

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with new features and fixes
3. **Run full test suite**: `pytest`
4. **Build package**: `python -m build`
5. **Create GitHub release** with tag
6. **Deploy documentation**: `mkdocs gh-deploy`

## 🤝 Contributing

### Getting Started

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with tests
4. **Run the test suite**: `pytest`
5. **Submit a pull request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8 and use Black for formatting
- **Tests**: Include tests for new features and bug fixes
- **Documentation**: Update documentation for new features
- **Commit Messages**: Use clear, descriptive commit messages
- **Pull Requests**: Include description of changes and testing done

### Adding New Toolkits

To add a new toolkit:

1. **Create the toolkit file** in `src/enhancedtoolkits/`
2. **Inherit from StrictToolkit**
3. **Implement required methods** with proper validation
4. **Add comprehensive tests**
5. **Update documentation**
6. **Add to `__init__.py`** exports

Example:

```python
# src/enhancedtoolkits/my_toolkit.py
from .base import StrictToolkit

class MyToolkit(StrictToolkit):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def my_method(self, param: str) -> str:
        """Method description."""
        try:
            # Validate inputs
            if not param:
                raise ValueError("param cannot be empty")
            
            # Perform operation
            result = self._process(param)
            
            # Return formatted result
            return self._format_response(result)
            
        except Exception as e:
            return self._handle_error("my_method", e)
```

## 📚 Resources

### Documentation
- [Core Toolkits](../toolkits/index.md) - Detailed toolkit documentation
- [Calculator Modules](../calculators/index.md) - Calculator documentation
- [API Reference](../api/index.md) - Complete API documentation

### External Resources
- [Agno Framework](https://github.com/agno-ai/agno) - AI agent framework
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) - Function calling guide
- [Python Packaging](https://packaging.python.org/) - Python packaging guide

### Community
- [GitHub Issues](https://github.com/malvavisc0/enhancedtoolkits/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions) - Community discussions
- [Contributing Guide](contributing.md) - Detailed contribution guidelines

## 🆘 Getting Help

- **Documentation Issues**: Check existing docs or open an issue
- **Bug Reports**: Use GitHub issues with detailed reproduction steps
- **Feature Requests**: Discuss in GitHub discussions first
- **Development Questions**: Join community discussions

---

Thank you for contributing to Enhanced Toolkits! 🚀
