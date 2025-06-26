# Investment Analysis Calculator

Advanced investment analysis tools for portfolio optimization and risk assessment.

## Overview

The Investment Analysis Calculator provides comprehensive tools for analyzing investment opportunities, portfolio performance, and risk metrics.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import InvestmentAnalysisCalculatorTools

# Add to agent
agent = Agent(
    name="Investment Analyst",
    model="gpt-4",
    tools=[InvestmentAnalysisCalculatorTools()]
)
```

## Available Functions

### Return Analysis
- `calculate_roi()` - Return on investment calculations
- `calculate_cagr()` - Compound annual growth rate
- `calculate_sharpe_ratio()` - Risk-adjusted returns

### Portfolio Analysis
- `calculate_portfolio_return()` - Weighted portfolio returns
- `calculate_portfolio_risk()` - Portfolio volatility and risk
- `optimize_portfolio()` - Portfolio optimization algorithms

### Valuation Models
- `calculate_dcf()` - Discounted cash flow valuation
- `calculate_capm()` - Capital asset pricing model
- `calculate_wacc()` - Weighted average cost of capital

## Example Usage

```python
# Agent automatically has access to these functions
response = agent.run(
    "Calculate the Sharpe ratio for a portfolio with 12% return, 8% risk-free rate, and 15% volatility"
)
```

## Related Tools

- [Time Value Calculator](time-value.md)
- [Risk Metrics Calculator](risk.md)
- [Bond Calculator](bond.md)