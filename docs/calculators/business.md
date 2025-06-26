# Business Analysis Calculator

Business metrics and financial analysis tools for enterprise decision making.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import BusinessAnalysisCalculatorTools

agent = Agent(
    name="Business Analyst",
    model="gpt-4",
    tools=[BusinessAnalysisCalculatorTools()]
)
```

## Available Functions

- `calculate_break_even()` - Break-even analysis
- `calculate_cash_flow()` - Cash flow projections
- `calculate_profitability_ratios()` - ROE, ROA, profit margins
- `calculate_liquidity_ratios()` - Current ratio, quick ratio

## Related Tools

- [Investment Calculator](investment.md)
- [Depreciation Calculator](depreciation.md)