# Risk Metrics Calculator

Financial risk assessment and portfolio risk analysis tools.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import RiskMetricsCalculatorTools

agent = Agent(
    name="Risk Analyst",
    model="gpt-4",
    tools=[RiskMetricsCalculatorTools()]
)
```

## Available Functions

- `calculate_var()` - Value at Risk calculations
- `calculate_beta()` - Beta coefficient analysis
- `calculate_volatility()` - Historical and implied volatility
- `calculate_correlation()` - Asset correlation analysis

## Related Tools

- [Investment Calculator](investment.md)
- [Bond Calculator](bond.md)