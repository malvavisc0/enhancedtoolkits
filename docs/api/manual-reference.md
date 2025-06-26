# Manual API Reference

This page provides API documentation that doesn't require module imports, useful for development and when the module isn't installed.

## Core Toolkits

### ReasoningTools

```python
class EnhancedReasoningTools(StrictToolkit):
    """Multi-modal reasoning tools with cognitive bias detection."""
    
    def __init__(
        self,
        reasoning_depth: int = 5,
        enable_bias_detection: bool = True,
        instructions: Optional[str] = None
    ):
        """Initialize reasoning tools."""
    
    def reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_type: str,
        evidence: List[str],
        context: Optional[str] = None
    ) -> str:
        """Apply specific reasoning type to a problem."""
    
    def multi_modal_reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_types: List[str],
        evidence: List[str]
    ) -> str:
        """Combine multiple reasoning approaches."""
    
    def analyze_reasoning(
        self,
        agent_or_team: Any,
        reasoning_content: str,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """Evaluate reasoning results."""
    
    def detect_biases(
        self,
        agent_or_team: Any,
        reasoning_content: str
    ) -> str:
        """Identify cognitive biases."""
    
    def get_reasoning_history(
        self,
        agent_or_team: Any
    ) -> str:
        """Retrieve session reasoning history."""
```

### YFinanceTools

```python
class EnhancedYFinanceTools(StrictToolkit):
    """Comprehensive financial data retrieval."""
    
    def __init__(
        self,
        enable_caching: bool = True,
        cache_ttl: int = 300,
        rate_limit_delay: float = 0.1
    ):
        """Initialize finance tools."""
    
    def get_current_price(self, ticker: str) -> str:
        """Get current stock price with change data."""
    
    def get_company_information(self, ticker: str) -> str:
        """Get comprehensive company details."""
    
    def get_news_for_ticker(
        self,
        ticker: str,
        max_articles: int = 10
    ) -> str:
        """Get latest news articles."""
    
    def get_earnings_history(self, ticker: str) -> str:
        """Get historical earnings data."""
    
    def get_income_statement(self, ticker: str) -> str:
        """Get annual income statement."""
    
    def get_balance_sheet(self, ticker: str) -> str:
        """Get balance sheet information."""
    
    def get_cashflow(self, ticker: str) -> str:
        """Get cash flow statements."""
```

## Calculator Modules

### ArithmeticCalculatorTools

```python
class ArithmeticCalculatorTools:
    """Basic arithmetic operations with validation."""
    
    def add(self, a: float, b: float) -> str:
        """Add two numbers."""
    
    def subtract(self, a: float, b: float) -> str:
        """Subtract second number from first."""
    
    def multiply(self, a: float, b: float) -> str:
        """Multiply two numbers."""
    
    def divide(self, a: float, b: float) -> str:
        """Divide first number by second."""
    
    def exponentiate(self, base: float, exponent: float) -> str:
        """Raise base to power of exponent."""
    
    def square_root(self, number: float) -> str:
        """Calculate square root."""
    
    def factorial(self, n: int) -> str:
        """Calculate factorial of non-negative integer."""
    
    def is_prime(self, number: int) -> str:
        """Check if number is prime."""
```

### TimeValueCalculatorTools

```python
class TimeValueCalculatorTools:
    """Time value of money calculations."""
    
    def calculate_present_value(
        self,
        future_value: float,
        rate: float,
        periods: int
    ) -> str:
        """Calculate present value of future sum."""
    
    def calculate_future_value(
        self,
        present_value: float,
        rate: float,
        periods: int
    ) -> str:
        """Calculate future value of present sum."""
    
    def calculate_annuity_present_value(
        self,
        payment: float,
        rate: float,
        periods: int
    ) -> str:
        """Calculate present value of annuity."""
    
    def calculate_annuity_future_value(
        self,
        payment: float,
        rate: float,
        periods: int
    ) -> str:
        """Calculate future value of annuity."""
    
    def calculate_perpetuity_value(
        self,
        payment: float,
        rate: float
    ) -> str:
        """Calculate present value of perpetuity."""
```

## Base Classes

### StrictToolkit

```python
class StrictToolkit(Toolkit):
    """Base class ensuring OpenAI compatibility."""
    
    def register(
        self,
        function: Callable[..., Any],
        name: Optional[str] = None
    ) -> None:
        """Register function with strict parameter validation."""
    
    def _validate_openai_compatibility(
        self,
        function: Callable[..., Any]
    ) -> None:
        """Validate OpenAI function calling compatibility."""
```

## Usage Examples

### Basic Usage
```python
from enhancedtoolkits import (
    ReasoningTools,
    YFinanceTools,
    CalculatorTools
)

# Initialize tools
reasoning = ReasoningTools()
finance = YFinanceTools()
calculator = CalculatorTools()

# Use reasoning
result = reasoning.reason(
    agent_or_team=agent,
    problem="Investment decision",
    reasoning_type="analytical",
    evidence=["Market data", "Financial metrics"]
)

# Get financial data
price = finance.get_current_price("AAPL")

# Perform calculations
payment = calculator.calculate_loan_payment(
    principal=100000,
    annual_rate=0.05,
    years=30
)
```

### Error Handling
```python
try:
    result = calculator.divide(10, 0)
except ZeroDivisionError as e:
    print(f"Division error: {e}")

try:
    price = finance.get_current_price("INVALID")
except Exception as e:
    print(f"Finance error: {e}")
```

This manual reference provides the API structure without requiring module imports, ensuring the documentation builds successfully even when the module isn't installed in the documentation environment.