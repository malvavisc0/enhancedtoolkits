# Loan Calculator

Comprehensive loan calculations for payments, amortization, and refinancing analysis.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import LoanCalculatorTools

agent = Agent(
    name="Loan Advisor",
    model="gpt-4",
    tools=[LoanCalculatorTools()]
)
```

## Available Functions

- `calculate_loan_payment()` - Monthly payment calculations
- `calculate_amortization_schedule()` - Payment breakdown over time
- `calculate_loan_balance()` - Remaining balance calculations
- `calculate_refinance_savings()` - Refinancing analysis

## Related Tools

- [Time Value Calculator](time-value.md)
- [Investment Calculator](investment.md)