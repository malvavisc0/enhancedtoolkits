# Depreciation Calculator API Reference

API documentation for the Depreciation Calculator – tools for calculating asset depreciation using straight-line and declining balance methods.

## Class: DepreciationCalculatorTools

Provides depreciation calculations for assets, including straight-line and declining balance methods.

### DepreciationCalculatorTools()

Initialize the Depreciation Calculator toolkit.

**Parameters:**
- `add_instructions` (bool, optional): Whether to include LLM usage instructions. Default: True
- `instructions` (str, optional): Custom instructions for LLMs. Default: Built-in instructions

### Methods

#### calculate_straight_line_depreciation()

Calculate annual depreciation using the straight-line method.

**Parameters:**
- `cost` (float): Initial cost of the asset (e.g., 50000.0)
- `salvage` (float): Salvage value at end of useful life (e.g., 5000.0)
- `life` (int): Useful life in years (e.g., 10)

**Returns:**
- `str` (JSON): Depreciation calculation including annual depreciation, total depreciation, depreciation rate, and schedule.

**Raises:**
- `FinancialValidationError`: If salvage value is not less than cost.
- `FinancialComputationError`: For unexpected calculation errors.

#### calculate_declining_balance_depreciation()

Calculate depreciation using the declining balance method.

**Parameters:**
- `cost` (float): Initial cost of the asset (e.g., 30000.0)
- `rate` (float): Depreciation rate per period as decimal (e.g., 0.20)
- `life` (int): Useful life in years (e.g., 5)

**Returns:**
- `str` (JSON): Depreciation calculation including total depreciation, final book value, and schedule.

**Raises:**
- `FinancialValidationError`: For invalid input values.
- `FinancialComputationError`: For unexpected calculation errors.

### Usage Example

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import DepreciationCalculatorTools

# Initialize calculator
depr_calc = DepreciationCalculatorTools()

# Add to agent
agent = Agent(
    name="Depreciation Analyst",
    model="gpt-4",
    tools=[depr_calc]
)

# Agent can now perform depreciation analysis
response = agent.run(
    "Calculate straight-line depreciation for an asset costing $50,000, salvage value $5,000, life 10 years"
)
```

## Depreciation Metrics

- **Straight-Line Depreciation**: Equal annual depreciation over asset's useful life.
- **Declining Balance Depreciation**: Accelerated depreciation, higher in early years.
- **Depreciation Schedule**: Year-by-year breakdown of depreciation, accumulated depreciation, and book value.

## Related Documentation

- [Depreciation Calculator Guide](../../calculators/depreciation.md)
- [Calculator Base Classes](../base.md)
