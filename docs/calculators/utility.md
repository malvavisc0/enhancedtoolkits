# Utility Calculator

General-purpose mathematical and statistical calculations for various applications.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import UtilityCalculatorTools

agent = Agent(
    name="Data Analyst",
    model="gpt-4",
    tools=[UtilityCalculatorTools()]
)
```

## Available Functions

- `calculate_statistics()` - Mean, median, mode, standard deviation
- `calculate_percentiles()` - Quartiles and percentile calculations
- `calculate_correlation()` - Correlation coefficients
- `calculate_regression()` - Linear and polynomial regression

## Related Tools

- [Arithmetic Calculator](arithmetic.md)
- [Business Analysis Calculator](business.md)