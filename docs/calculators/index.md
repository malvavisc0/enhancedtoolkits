# Calculator Modules for AI Agents

Enhanced Toolkits provides **9 specialized calculator modules** designed for AI agents that need mathematical and financial calculation capabilities.

## 🤖 AI Agent Integration

All calculator modules follow the same pattern for AI agent integration:

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import CalculatorName

# Create agent with calculator (Agno handles registration automatically)
agent = Agent(
    name="Your Agent",
    model="gpt-4",
    tools=[CalculatorName()]
)

# Agent automatically has access to all calculator functions
```

## 🧮 Available Calculator Modules

### 🔢 Arithmetic Calculator
**Basic mathematical operations with validation**

```python
from enhancedtoolkits.calculators import ArithmeticCalculatorTools

arithmetic = ArithmeticCalculatorTools()
```

**Functions available to agents:**
- `add()`, `subtract()`, `multiply()`, `divide()`
- `exponentiate()`, `square_root()`, `factorial()`
- `is_prime()` - Prime number checking

[Setup Guide →](arithmetic.md)

---

### ⏰ Time Value Calculator
**Time value of money calculations for financial planning**

```python
from enhancedtoolkits.calculators import TimeValueCalculatorTools

time_value = TimeValueCalculatorTools()
```

**Functions available to agents:**
- `calculate_present_value()` - Discount future cash flows
- `calculate_future_value()` - Compound present values
- `calculate_annuity_present_value()` - Present value of annuities
- `calculate_annuity_future_value()` - Future value of annuities
- `calculate_perpetuity_value()` - Present value of perpetuities

[Setup Guide →](time-value.md)

---

### 📊 Investment Analysis Calculator
**Investment evaluation and analysis tools**

```python
from enhancedtoolkits.calculators import InvestmentAnalysisCalculatorTools

investment = InvestmentAnalysisCalculatorTools()
```

**Functions available to agents:**
- `calculate_net_present_value()` - NPV of cash flows
- `calculate_internal_rate_of_return()` - IRR calculations
- `calculate_compound_annual_growth_rate()` - CAGR analysis
- `calculate_return_on_investment()` - ROI calculations

[Setup Guide →](investment.md)

---

### 🏠 Loan Calculator
**Loan analysis and payment calculations**

```python
from enhancedtoolkits.calculators import LoanCalculatorTools

loan = LoanCalculatorTools()
```

**Functions available to agents:**
- `calculate_loan_payment()` - Monthly payment calculations
- `generate_amortization_schedule()` - Complete payment schedules
- `calculate_total_interest()` - Total interest over loan term
- `calculate_remaining_balance()` - Outstanding loan balance

[Setup Guide →](loan.md)

---

### 💰 Bond Calculator
**Bond valuation and yield calculations**

```python
from enhancedtoolkits.calculators import BondCalculatorTools

bond = BondCalculatorTools()
```

**Functions available to agents:**
- `calculate_bond_price()` - Bond pricing based on cash flows
- `calculate_yield_to_maturity()` - YTM calculations
- `calculate_duration()` - Bond duration analysis
- `calculate_convexity()` - Price sensitivity measures

[Setup Guide →](bond.md)

---

### 📈 Risk Metrics Calculator
**Risk assessment and portfolio analysis**

```python
from enhancedtoolkits.calculators import RiskMetricsCalculatorTools

risk = RiskMetricsCalculatorTools()
```

**Functions available to agents:**
- `calculate_sharpe_ratio()` - Risk-adjusted returns
- `calculate_volatility()` - Standard deviation of returns
- `calculate_beta()` - Market sensitivity analysis
- `calculate_value_at_risk()` - VaR calculations

[Setup Guide →](risk.md)

---

### 📉 Depreciation Calculator
**Asset depreciation and tax calculations**

```python
from enhancedtoolkits.calculators import DepreciationCalculatorTools

depreciation = DepreciationCalculatorTools()
```

**Functions available to agents:**
- `calculate_straight_line_depreciation()` - Linear depreciation
- `calculate_declining_balance_depreciation()` - Accelerated depreciation
- `calculate_sum_of_years_digits()` - Alternative depreciation method
- `generate_depreciation_schedule()` - Multi-year schedules

[Setup Guide →](depreciation.md)

---

### 🏢 Business Analysis Calculator
**Business financial analysis and planning**

```python
from enhancedtoolkits.calculators import BusinessAnalysisCalculatorTools

business = BusinessAnalysisCalculatorTools()
```

**Functions available to agents:**
- `calculate_break_even_point()` - Break-even analysis

<!-- The following functions are not currently implemented:
- `calculate_profit_margin()` - Profitability metrics
- `calculate_cost_volume_profit()` - CVP analysis
- `calculate_financial_ratios()` - Key business ratios
-->

[Setup Guide →](business.md)

---

### 🔧 Utility Calculator
**Currency conversion and inflation adjustments**

```python
from enhancedtoolkits.calculators import UtilityCalculatorTools

utility = UtilityCalculatorTools()
```

**Functions available to agents:**
- `convert_currency()` - Currency conversion with exchange rates
- `adjust_for_inflation()` - Inflation-adjusted calculations

<!-- The following functions are not currently implemented:
- `calculate_tax()` - Tax calculations
- `calculate_percentage()` - Percentage operations
-->

[Setup Guide →](utility.md)

---

## 🔧 Complete AI Agent Setup

### All Calculator Modules
```python
from agno.agent import Agent
from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
    InvestmentAnalysisCalculatorTools,
    LoanCalculatorTools,
    BondCalculatorTools,
    RiskMetricsCalculatorTools,
    DepreciationCalculatorTools,
    BusinessAnalysisCalculatorTools,
    UtilityCalculatorTools
)

# Create agent with all calculator modules
agent = Agent(
    name="Financial Calculator Agent",
    model="gpt-4",
    tools=[
        ArithmeticCalculatorTools(),
        TimeValueCalculatorTools(),
        InvestmentAnalysisCalculatorTools(),
        LoanCalculatorTools(),
        BondCalculatorTools(),
        RiskMetricsCalculatorTools(),
        DepreciationCalculatorTools(),
        BusinessAnalysisCalculatorTools(),
        UtilityCalculatorTools()
    ]
)
```

### Selective Calculator Setup
```python
from agno.agent import Agent
from enhancedtoolkits.calculators import *

# Create agent with only financial calculators
agent = Agent(
    name="Financial Analyst",
    model="gpt-4",
    tools=[
        TimeValueCalculatorTools(),
        InvestmentAnalysisCalculatorTools(),
        LoanCalculatorTools(),
        BondCalculatorTools()
    ]
)
```

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits.calculators import InvestmentAnalysisCalculatorTools

investment = InvestmentAnalysisCalculatorTools()

# Get function schema for OpenAI
tools = [investment.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Calculate the NPV of this investment: initial cost $100k, annual returns $25k for 5 years, discount rate 10%"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits.calculators import *

agent = Agent(
    name="Financial Analyst",
    model="gpt-4",
    tools=[
        ArithmeticCalculatorTools(),
        TimeValueCalculatorTools(),
        InvestmentAnalysisCalculatorTools(),
        LoanCalculatorTools()
    ]
)

# Agent automatically has access to all calculator functions
response = agent.run("Analyze this investment opportunity and calculate loan payments for financing")
```

## 🛡️ Features

All calculator modules include:
- **Input validation** and type checking
- **Comprehensive error handling** with detailed messages
- **Mathematical precision** for financial calculations
- **Consistent output format** for AI agent consumption
- **OpenAI compatibility** out of the box

## 📊 Example Agent Interactions

**Agent Query:** "Calculate monthly payment for a $300k mortgage at 6% for 30 years"

**Calculator Response:**
```json
{
  "monthly_payment": "$1,798.65",
  "total_interest": "$347,514.57",
  "total_payments": "$647,514.57"
}
```

**Agent Query:** "What's the NPV of investing $50k now to get $15k annually for 5 years at 8% discount rate?"

**Calculator Response:**
```json
{
  "npv": "$9,927.25",
  "recommendation": "Positive NPV - investment is profitable",
  "irr": "15.24%"
}
```

## 🚀 Next Steps

1. **Choose the calculator modules** your AI agent needs
2. **Follow the setup guides** for each calculator
3. **Register with your AI agent** using OpenAI or Agno
4. **Test calculations** with sample queries
5. **Monitor performance** and accuracy

Each calculator module provides specialized financial and mathematical capabilities that enable your AI agent to perform complex calculations reliably and accurately.
