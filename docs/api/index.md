# API Reference

Welcome to the Enhanced Toolkits API Reference! This section provides comprehensive documentation for all classes, methods, and functions in the Enhanced Toolkits library, automatically generated from the source code.

## 📚 Documentation Structure

### Core Toolkits
Complete API documentation for all 8 core toolkits:

- **[Reasoning Tools](reasoning.md)** - Multi-modal reasoning with bias detection
- **[Search Tools](searxng.md)** - Web search with content extraction  
- **[Thinking Tools](thinking.md)** - Structured cognitive frameworks
- **[Files Tools](files.md)** - Enterprise-grade file operations
- **[Finance Tools](finance.md)** - Comprehensive financial data
- **[YouTube Tools](youtube.md)** - Video metadata and transcripts
- **[Weather Tools](weather.md)** - Weather data and forecasts
- **[Downloader Tools](downloader.md)** - Universal file downloading

### Calculator Modules
API documentation for all 9 calculator modules:

- **[Arithmetic Calculator](calculators/arithmetic.md)** - Basic mathematical operations
- **[Time Value Calculator](calculators/time-value.md)** - Time value of money calculations
- **[Investment Analysis](calculators/investment.md)** - NPV, IRR, CAGR calculations
- **[Loan Calculator](calculators/loan.md)** - Loan payments and amortization
- **[Bond Calculator](calculators/bond.md)** - Bond pricing and yield calculations
- **[Risk Metrics Calculator](calculators/risk.md)** - Risk assessment tools
- **[Depreciation Calculator](calculators/depreciation.md)** - Asset depreciation methods
- **[Business Analysis Calculator](calculators/business.md)** - Business financial analysis
- **[Utility Calculator](calculators/utility.md)** - Currency and inflation adjustments

### Base Classes
Foundation classes that power all toolkits:

- **[StrictToolkit](base.md)** - Base class for all toolkits
- **[Calculator Base](base.md)** - Base classes for calculator modules

## 🔍 How to Use This Reference

### Navigation
- **Browse by Category**: Use the navigation menu to explore different toolkit categories
- **Search**: Use the search function to find specific methods or classes
- **Cross-References**: Click on linked types and methods to navigate between related components

### Method Documentation
Each method includes:
- **Signature**: Complete method signature with type annotations
- **Parameters**: Detailed parameter descriptions and types
- **Returns**: Return value description and type
- **Raises**: Possible exceptions and when they occur
- **Examples**: Code examples showing usage
- **Source Code**: Optional source code viewing

### Code Examples
All examples are ready to run:

```python
from enhancedtoolkits import ReasoningTools

# Initialize toolkit
reasoning = ReasoningTools()

# Use methods as documented
result = reasoning.reason(
    agent_or_team=agent,
    problem="Your problem here",
    reasoning_type="analytical",
    evidence=["Evidence 1", "Evidence 2"]
)
```

## 🚀 Quick Reference

### Common Import Patterns

```python
# Import all main toolkits
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    WeatherTools,
    DownloaderTools,
    CalculatorTools
)

# Import specific calculator modules
from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
    InvestmentAnalysisCalculatorTools
)

# Import base classes for custom development
from enhancedtoolkits.base import StrictToolkit
```

### Initialization Patterns

```python
# Basic initialization
toolkit = ToolkitName()

# With configuration
toolkit = ToolkitName(
    enable_caching=True,
    timeout=30,
    rate_limit_delay=0.1
)

# Calculator tools (unified interface)
calculator = CalculatorTools()
```

### Error Handling Patterns

```python
from enhancedtoolkits.exceptions import (
    ToolkitError,
    ValidationError,
    APIError
)

try:
    result = toolkit.method_name(param="value")
except ValidationError as e:
    print(f"Input validation failed: {e}")
except APIError as e:
    print(f"API call failed: {e}")
except ToolkitError as e:
    print(f"Toolkit error: {e}")
```

## 📖 Documentation Features

### Automatic Generation
This API documentation is automatically generated from the source code using [MkDocstrings](https://mkdocstrings.github.io/), ensuring it's always up-to-date with the latest code.

### Type Information
All methods include complete type information from Python type annotations, making it easy to understand expected inputs and outputs.

### Interactive Examples
Code examples are syntax-highlighted and can be copied directly for use in your projects.

### Cross-References
Related methods and classes are automatically linked, making it easy to explore the API.

## 🔗 Related Documentation

- **[Getting Started](../getting-started/index.md)** - Installation and quick start guide
- **[Core Toolkits](../toolkits/index.md)** - High-level toolkit documentation with examples
- **[Calculator Modules](../calculators/index.md)** - Calculator documentation with use cases
- **[Developer Guide](../developer/index.md)** - Contributing and development information

## 📝 Feedback

Found an issue with the API documentation? Please:

- **Report bugs**: [GitHub Issues](https://github.com/malvavisc0/enhancedtoolkits/issues)
- **Suggest improvements**: [GitHub Discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions)
- **Contribute**: See our [Developer Guide](../developer/index.md)

---

**Note**: This API reference is automatically generated from docstrings in the source code. For conceptual documentation and tutorials, see the [Core Toolkits](../toolkits/index.md) and [Calculator Modules](../calculators/index.md) sections.
