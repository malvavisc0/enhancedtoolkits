# Loan Calculator API Reference

API documentation for the Loan Calculator - comprehensive loan calculations for payments, amortization, and refinancing analysis.

## Class: LoanCalculatorTools

Loan calculation toolkit providing comprehensive tools for loan payments, amortization schedules, and refinancing analysis.

### LoanCalculatorTools()

Initialize the Loan Calculator toolkit.

### Methods

#### calculate_loan_payment()

Calculate monthly loan payment amount.

**Parameters:**
- `principal` (float): Loan principal amount
- `annual_rate` (float): Annual interest rate percentage
- `years` (int): Loan term in years
- `payment_frequency` (str): Payment frequency ('monthly', 'quarterly', 'annually')

**Returns:**
- `dict`: Monthly payment calculation with breakdown

#### calculate_amortization_schedule()

Generate complete amortization schedule for a loan.

**Parameters:**
- `principal` (float): Loan principal amount
- `annual_rate` (float): Annual interest rate percentage
- `years` (int): Loan term in years
- `extra_payment` (float, optional): Additional monthly payment

**Returns:**
- `dict`: Complete amortization schedule with payment breakdown

#### calculate_loan_balance()

Calculate remaining loan balance at any point.

**Parameters:**
- `principal` (float): Original loan principal
- `annual_rate` (float): Annual interest rate percentage
- `years` (int): Original loan term in years
- `payments_made` (int): Number of payments already made

**Returns:**
- `dict`: Remaining balance and loan details

#### calculate_refinance_savings()

Analyze potential savings from loan refinancing.

**Parameters:**
- `current_balance` (float): Current loan balance
- `current_rate` (float): Current interest rate percentage
- `new_rate` (float): New interest rate percentage
- `remaining_years` (int): Remaining years on current loan
- `new_years` (int): New loan term in years
- `closing_costs` (float): Refinancing closing costs

**Returns:**
- `dict`: Refinancing analysis with savings calculation

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import LoanCalculatorTools

agent = Agent(
    name="Loan Advisor",
    model="gpt-4",
    tools=[LoanCalculatorTools()]
)
```

## Related Documentation

- [Loan Calculator Guide](../../calculators/loan.md)
- [Time Value Calculator API](time-value.md)
- [Investment Calculator API](investment.md)