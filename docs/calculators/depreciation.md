# Depreciation Calculator

Asset depreciation calculations for accounting and tax purposes.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import DepreciationCalculatorTools

agent = Agent(
    name="Accounting Assistant",
    model="gpt-4",
    tools=[DepreciationCalculatorTools()]
)
```

## Available Functions

- `calculate_straight_line()` - Straight-line depreciation
- `calculate_declining_balance()` - Declining balance method
- `calculate_sum_of_years()` - Sum-of-years-digits method
- `calculate_units_of_production()` - Units of production method

## Related Tools

- [Business Analysis Calculator](business.md)
- [Utility Calculator](utility.md)