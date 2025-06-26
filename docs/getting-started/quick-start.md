# Quick Start Guide

Get up and running with Enhanced Toolkits in just a few minutes!

## Prerequisites

- Python 3.8+
- Enhanced Toolkits installed ([Installation Guide](installation.md))

## Your First Enhanced Toolkits Program

### 1. Basic Setup

```python
from enhancedtoolkits import (
    ReasoningTools,
    CalculatorTools,
    YFinanceTools
)

# Initialize tools
reasoning = ReasoningTools()
calculator = CalculatorTools()
finance = YFinanceTools()
```

### 2. Simple Calculation

```python
# Basic arithmetic
result = calculator.add(10, 5)
print(f"10 + 5 = {result}")

# Financial calculation
loan_payment = calculator.calculate_loan_payment(
    principal=100000,
    annual_rate=0.05,
    years=30
)
print(f"Monthly payment: ${loan_payment}")
```

### 3. Reasoning Example

```python
# Use reasoning tools
reasoning_result = reasoning.reason(
    agent_or_team=None,  # Your agent instance
    problem="Should I invest in renewable energy stocks?",
    reasoning_type="analytical",
    evidence=[
        "Government incentives for clean energy",
        "Growing market demand",
        "Technological improvements"
    ]
)
print(reasoning_result)
```

### 4. Financial Data

```python
# Get stock information
stock_info = finance.get_current_price("AAPL")
print(f"Apple stock info: {stock_info}")

company_info = finance.get_company_information("TSLA")
print(f"Tesla company info: {company_info}")
```

## Complete Example

Here's a complete example that demonstrates multiple toolkits:

```python
from enhancedtoolkits import (
    ReasoningTools,
    CalculatorTools,
    YFinanceTools,
    WeatherTools
)
import json

def investment_advisor():
    # Initialize tools
    reasoning = ReasoningTools()
    calculator = CalculatorTools()
    finance = YFinanceTools()
    weather = WeatherTools()
    
    # Get financial data
    print("📈 Getting stock information...")
    apple_price = finance.get_current_price("AAPL")
    
    # Calculate investment scenarios
    print("🧮 Calculating investment scenarios...")
    future_value = calculator.calculate_future_value(
        present_value=10000,
        rate=0.07,
        periods=10
    )
    
    # Use reasoning for decision making
    print("🧠 Analyzing investment decision...")
    reasoning_result = reasoning.reason(
        agent_or_team=None,
        problem="Should I invest $10,000 in Apple stock?",
        reasoning_type="analytical",
        evidence=[
            f"Current Apple price data: {apple_price}",
            f"Expected future value at 7% return: ${future_value}",
            "Apple's strong market position",
            "Technology sector growth trends"
        ]
    )
    
    print("\n" + "="*50)
    print("INVESTMENT ANALYSIS REPORT")
    print("="*50)
    print(f"Apple Stock Info: {apple_price}")
    print(f"Future Value Projection: ${future_value}")
    print(f"Reasoning Analysis: {reasoning_result}")

if __name__ == "__main__":
    investment_advisor()
```

## Next Steps

Now that you have Enhanced Toolkits working:

1. **Explore Core Toolkits**: Learn about all [available toolkits](../toolkits/index.md)
2. **Try Calculator Modules**: Experiment with [financial calculators](../calculators/index.md)
3. **Configure Environment**: Set up [environment variables](configuration.md)
4. **Build Your Agent**: Integrate with your AI agent framework

## Common Patterns

### Error Handling

```python
try:
    result = finance.get_current_price("INVALID_TICKER")
except Exception as e:
    print(f"Error: {e}")
```

### Configuration

```python
# Configure tools with custom settings
finance_tool = YFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)
```

### Batch Operations

```python
# Process multiple stocks
tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]
for ticker in tickers:
    price_info = finance.get_current_price(ticker)
    print(f"{ticker}: {price_info}")
```

## Troubleshooting

**Import Error**: Make sure Enhanced Toolkits is installed correctly
```bash
pip list | grep enhancedtoolkits
```

**API Errors**: Check your internet connection and API rate limits

**Performance**: Enable caching for frequently accessed data

## Getting Help

- 📖 [Full Documentation](../toolkits/index.md)
- 🐛 [Report Issues](https://github.com/malvavisc0/enhancedtoolkits/issues)
- 💬 [Community Discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions)

Ready to build something amazing? Let's go! 🚀
