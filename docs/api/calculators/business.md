# Business Analysis Calculator API Reference

API documentation for the Business Analysis Calculator – tools for business analysis including break-even point calculations.

## Class: BusinessAnalysisCalculatorTools

Provides business analysis calculations such as break-even point analysis for businesses and entrepreneurs.

### BusinessAnalysisCalculatorTools()

Initialize the Business Analysis Calculator toolkit.

**Parameters:**
- `add_instructions` (bool, optional): Whether to include LLM usage instructions. Default: True
- `instructions` (str, optional): Custom instructions for LLMs. Default: Built-in instructions

### Methods

#### calculate_break_even_point()

Calculate the break-even point in units and sales.

**Parameters:**
- `fixed_costs` (float): Total fixed costs (e.g., 10000.0)
- `price_per_unit` (float): Selling price per unit (e.g., 25.0)
- `variable_cost_per_unit` (float): Variable cost per unit (e.g., 15.0)

**Returns:**
- `str` (JSON): Break-even analysis including break-even units, sales, contribution margin, and ratio.

**Raises:**
- `FinancialValidationError`: If price per unit is not greater than variable cost per unit.
- `FinancialComputationError`: For unexpected calculation errors.

### Usage Example

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import BusinessAnalysisCalculatorTools

# Initialize calculator
business_calc = BusinessAnalysisCalculatorTools()

# Add to agent
agent = Agent(
    name="Business Analyst",
    model="gpt-4",
    tools=[business_calc]
)

# Agent can now perform business analysis
response = agent.run(
    "Calculate the break-even point for fixed costs of $10,000, price per unit $25, variable cost per unit $15"
)
```

## Business Analysis Metrics

- **Break-even Point**: Number of units or sales needed to cover all fixed and variable costs.
- **Contribution Margin**: Difference between price per unit and variable cost per unit.
- **Contribution Margin Ratio**: Contribution margin as a percentage of price per unit.

## Related Documentation

- [Business Calculator Guide](../../calculators/business.md)
- [Calculator Base Classes](../base.md)
