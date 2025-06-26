# Investment Analysis Calculator API Reference

API documentation for the Investment Analysis Calculator - advanced investment analysis tools for portfolio optimization and risk assessment.

## Class: InvestmentAnalysisCalculatorTools

Advanced investment analysis toolkit providing comprehensive tools for analyzing investment opportunities, portfolio performance, and risk metrics.

### InvestmentAnalysisCalculatorTools()

Initialize the Investment Analysis Calculator toolkit.

**Parameters:**
- `enable_caching` (bool, optional): Enable response caching. Default: True
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: 300
- `precision` (int, optional): Decimal precision for calculations. Default: 4

### Methods

#### calculate_roi()

Calculate return on investment (ROI) for an investment.

**Parameters:**
- `initial_investment` (float): Initial investment amount
- `final_value` (float): Final investment value
- `time_period` (float): Investment time period in years

**Returns:**
- `dict`: ROI calculation with percentage return and annualized return

#### calculate_cagr()

Calculate compound annual growth rate (CAGR).

**Parameters:**
- `beginning_value` (float): Beginning investment value
- `ending_value` (float): Ending investment value
- `years` (float): Number of years

**Returns:**
- `dict`: CAGR calculation with compound annual growth rate

#### calculate_sharpe_ratio()

Calculate Sharpe ratio for risk-adjusted returns.

**Parameters:**
- `portfolio_return` (float): Portfolio return percentage
- `risk_free_rate` (float): Risk-free rate percentage
- `portfolio_volatility` (float): Portfolio volatility (standard deviation)

**Returns:**
- `dict`: Sharpe ratio calculation with risk-adjusted return metrics

#### calculate_portfolio_return()

Calculate weighted portfolio returns.

**Parameters:**
- `assets` (List[dict]): List of assets with weights and returns
- `rebalancing_frequency` (str): Rebalancing frequency ('monthly', 'quarterly', 'annually')

**Returns:**
- `dict`: Portfolio return calculation with weighted returns

#### calculate_portfolio_risk()

Calculate portfolio volatility and risk metrics.

**Parameters:**
- `assets` (List[dict]): List of assets with weights, returns, and correlations
- `correlation_matrix` (List[List[float]]): Asset correlation matrix

**Returns:**
- `dict`: Portfolio risk calculation with volatility and risk metrics

#### calculate_dcf()

Calculate discounted cash flow (DCF) valuation.

**Parameters:**
- `cash_flows` (List[float]): Projected cash flows
- `discount_rate` (float): Discount rate percentage
- `terminal_value` (float, optional): Terminal value

**Returns:**
- `dict`: DCF valuation with present value and terminal value

#### calculate_capm()

Calculate Capital Asset Pricing Model (CAPM) expected return.

**Parameters:**
- `risk_free_rate` (float): Risk-free rate percentage
- `beta` (float): Asset beta coefficient
- `market_return` (float): Expected market return percentage

**Returns:**
- `dict`: CAPM calculation with expected return

#### calculate_wacc()

Calculate Weighted Average Cost of Capital (WACC).

**Parameters:**
- `equity_value` (float): Market value of equity
- `debt_value` (float): Market value of debt
- `cost_of_equity` (float): Cost of equity percentage
- `cost_of_debt` (float): Cost of debt percentage
- `tax_rate` (float): Corporate tax rate percentage

**Returns:**
- `dict`: WACC calculation with weighted cost of capital

#### optimize_portfolio()

Optimize portfolio allocation using modern portfolio theory.

**Parameters:**
- `assets` (List[dict]): List of assets with expected returns and risks
- `correlation_matrix` (List[List[float]]): Asset correlation matrix
- `target_return` (float, optional): Target portfolio return
- `risk_tolerance` (str): Risk tolerance level ('conservative', 'moderate', 'aggressive')

**Returns:**
- `dict`: Optimized portfolio allocation with weights and expected metrics

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import InvestmentAnalysisCalculatorTools

# Initialize calculator
investment_calc = InvestmentAnalysisCalculatorTools()

# Add to agent
agent = Agent(
    name="Investment Analyst",
    model="gpt-4",
    tools=[investment_calc]
)

# Agent can now perform investment analysis
response = agent.run(
    "Calculate the Sharpe ratio for a portfolio with 12% return, 8% risk-free rate, and 15% volatility"
)
```

## Investment Metrics

### Return Metrics
- **ROI**: Return on Investment calculation
- **CAGR**: Compound Annual Growth Rate
- **Total Return**: Absolute and percentage returns
- **Risk-Adjusted Returns**: Sharpe ratio and other risk metrics

### Risk Metrics
- **Volatility**: Standard deviation of returns
- **Beta**: Systematic risk measure
- **Value at Risk (VaR)**: Potential loss estimation
- **Maximum Drawdown**: Largest peak-to-trough decline

### Valuation Models
- **DCF**: Discounted Cash Flow valuation
- **CAPM**: Capital Asset Pricing Model
- **WACC**: Weighted Average Cost of Capital
- **NPV**: Net Present Value calculations

## Related Documentation

- [Investment Calculator Guide](../../calculators/investment.md)
- [Time Value Calculator API](time-value.md)
- [Risk Metrics Calculator API](risk.md)
- [Calculator Base Classes](../base.md)
