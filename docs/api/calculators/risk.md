# Risk Metrics Calculator API Reference

API documentation for the Risk Metrics Calculator – tools for calculating risk metrics such as Sharpe ratio and volatility.

## Class: RiskMetricsCalculatorTools

Provides risk metrics calculations for investments, including Sharpe ratio and volatility.

### RiskMetricsCalculatorTools()

Initialize the Risk Metrics Calculator toolkit.

**Parameters:**
- `add_instructions` (bool, optional): Whether to include LLM usage instructions. Default: True
- `instructions` (str, optional): Custom instructions for LLMs. Default: Built-in instructions

### Methods

#### calculate_sharpe_ratio()

Calculate the Sharpe ratio for an investment.

**Parameters:**
- `returns` (List[float]): List of periodic returns as decimals (e.g., [0.10, 0.15, -0.05, 0.20])
- `risk_free_rate` (float): Risk-free rate per period as decimal (e.g., 0.02)

**Returns:**
- `str` (JSON): Sharpe ratio calculation including mean return, volatility, excess return, and summary.

**Raises:**
- `FinancialValidationError`: If fewer than 2 return observations are provided.
- `FinancialComputationError`: For calculation errors (e.g., zero volatility).

#### calculate_volatility()

Calculate the volatility (standard deviation) of returns.

**Parameters:**
- `returns` (List[float]): List of periodic returns as decimals (e.g., [0.08, 0.12, -0.03, 0.18])

**Returns:**
- `str` (JSON): Volatility calculation including mean return, variance, and summary.

**Raises:**
- `FinancialValidationError`: If fewer than 2 return observations are provided.
- `FinancialComputationError`: For unexpected calculation errors.

### Usage Example

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import RiskMetricsCalculatorTools

# Initialize calculator
risk_calc = RiskMetricsCalculatorTools()

# Add to agent
agent = Agent(
    name="Risk Analyst",
    model="gpt-4",
    tools=[risk_calc]
)

# Agent can now perform risk analysis
response = agent.run(
    "Calculate the Sharpe ratio for returns [0.10, 0.15, -0.05, 0.20] and risk-free rate 0.02"
)
```

## Risk Metrics

- **Sharpe Ratio**: Risk-adjusted return metric.
- **Volatility**: Standard deviation of returns.
- **Variance**: Measure of return dispersion.

## Related Documentation

- [Risk Calculator Guide](../../calculators/risk.md)
- [Calculator Base Classes](../base.md)
