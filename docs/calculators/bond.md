# Bond Calculator

Bond valuation, yield calculations, and fixed-income analysis tools.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import BondCalculatorTools

agent = Agent(
    name="Bond Analyst",
    model="gpt-4",
    tools=[BondCalculatorTools()]
)
```

## Available Functions

- `calculate_bond_price()` - Bond valuation calculations
- `calculate_bond_yield()` - Yield to maturity and current yield
- `calculate_duration()` - Modified and Macaulay duration
- `calculate_convexity()` - Bond convexity analysis

## Related Tools

- [Investment Calculator](investment.md)
- [Risk Metrics Calculator](risk.md)