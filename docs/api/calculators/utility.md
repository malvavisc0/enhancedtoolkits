# Utility Calculator API Reference

API documentation for the Utility Calculator – tools for currency conversion and inflation adjustment.

## Class: UtilityCalculatorTools

Provides utility calculations including currency conversion and inflation adjustments.

### UtilityCalculatorTools()

Initialize the Utility Calculator toolkit.

**Parameters:**
- `add_instructions` (bool, optional): Whether to include LLM usage instructions. Default: True
- `instructions` (str, optional): Custom instructions for LLMs. Default: Built-in instructions

### Methods

#### convert_currency()

Convert an amount from one currency to another using a given exchange rate.

**Parameters:**
- `amount` (float): Amount to convert (e.g., 1000.0)
- `rate` (float): Exchange rate (target per source, e.g., 1.25)

**Returns:**
- `str` (JSON): Currency conversion result including original and converted amounts, and exchange rate.

**Raises:**
- `FinancialValidationError`: For invalid input values.
- `FinancialComputationError`: For unexpected calculation errors.

#### adjust_for_inflation()

Adjust an amount for inflation over a number of periods.

**Parameters:**
- `amount` (float): Initial amount (e.g., 1000.0)
- `rate` (float): Inflation rate per period as decimal (e.g., 0.03)
- `periods` (int): Number of periods (e.g., 5)

**Returns:**
- `str` (JSON): Inflation adjustment result including adjusted amount, inflation impact, and purchasing power loss.

**Raises:**
- `FinancialValidationError`: For invalid input values.
- `FinancialComputationError`: For unexpected calculation errors.

### Usage Example

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import UtilityCalculatorTools

# Initialize calculator
utility_calc = UtilityCalculatorTools()

# Add to agent
agent = Agent(
    name="Utility Analyst",
    model="gpt-4",
    tools=[utility_calc]
)

# Agent can now perform utility calculations
response = agent.run(
    "Convert $1,000 to another currency at an exchange rate of 1.25"
)
```

## Utility Metrics

- **Currency Conversion**: Convert between currencies using a specified exchange rate.
- **Inflation Adjustment**: Adjust amounts for inflation over time.
- **Purchasing Power Loss**: Impact of inflation on original amount.

## Related Documentation

- [Utility Calculator Guide](../../calculators/utility.md)
- [Calculator Base Classes](../base.md)
