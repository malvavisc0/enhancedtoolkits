# Time Value Calculator

Financial time value calculations for present value, future value, and annuities.

## Overview

The Time Value Calculator provides essential financial calculations for time value of money, including present value, future value, and annuity calculations.

## Setup

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import TimeValueCalculatorTools

# Add to agent
agent = Agent(
    name="Financial Advisor",
    model="gpt-4",
    tools=[TimeValueCalculatorTools()]
)
```

## Available Functions

### Present Value Calculations
- `calculate_present_value()` - Calculate present value of future cash flows
- `calculate_present_value_annuity()` - Present value of annuity payments

### Future Value Calculations
- `calculate_future_value()` - Calculate future value of present amount
- `calculate_future_value_annuity()` - Future value of annuity payments

### Annuity Calculations
- `calculate_annuity_payment()` - Calculate periodic payment amount
- `calculate_annuity_periods()` - Calculate number of payment periods

## Example Usage

```python
# Agent automatically has access to these functions
response = agent.run(
    "Calculate the present value of $10,000 received in 5 years at 6% interest rate"
)
```

## Related Tools

- [Investment Calculator](investment.md)
- [Loan Calculator](loan.md)
- [Arithmetic Calculator](arithmetic.md)