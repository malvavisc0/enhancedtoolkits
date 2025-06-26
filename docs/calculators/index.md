# Calculator Modules

Enhanced Toolkits provides 9 specialized calculator modules for financial and mathematical calculations with comprehensive validation and error handling.

## Available Calculator Modules

<div class="toolkit-grid">
  <div class="toolkit-card">
    <h3>🔢 Arithmetic Calculator</h3>
    <p>Basic arithmetic operations with comprehensive validation.</p>
    <ul>
      <li>Add, subtract, multiply, divide</li>
      <li>Exponentiation and square root</li>
      <li>Factorial and prime checking</li>
      <li>Input validation and error handling</li>
    </ul>
    <a href="arithmetic/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>⏰ Time Value Calculator</h3>
    <p>Time value of money calculations for financial planning.</p>
    <ul>
      <li>Present and future value calculations</li>
      <li>Annuity valuations</li>
      <li>Perpetuity calculations</li>
      <li>Compound interest scenarios</li>
    </ul>
    <a href="time-value/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📊 Investment Analysis</h3>
    <p>Investment analysis tools for evaluating opportunities.</p>
    <ul>
      <li>Net Present Value (NPV)</li>
      <li>Internal Rate of Return (IRR)</li>
      <li>Compound Annual Growth Rate (CAGR)</li>
      <li>Return on Investment (ROI)</li>
    </ul>
    <a href="investment/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🏠 Loan Calculator</h3>
    <p>Loan analysis tools for payment calculations.</p>
    <ul>
      <li>Monthly payment calculations</li>
      <li>Amortization schedules</li>
      <li>Interest and principal breakdown</li>
      <li>Total interest calculations</li>
    </ul>
    <a href="loan/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>💰 Bond Calculator</h3>
    <p>Bond valuation tools for pricing and yield calculations.</p>
    <ul>
      <li>Bond price calculations</li>
      <li>Yield to Maturity (YTM)</li>
      <li>Duration and convexity</li>
      <li>Coupon payment analysis</li>
    </ul>
    <a href="bond/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📈 Risk Metrics</h3>
    <p>Risk assessment tools for investment analysis.</p>
    <ul>
      <li>Sharpe ratio calculations</li>
      <li>Volatility measurements</li>
      <li>Beta calculations</li>
      <li>Value at Risk (VaR)</li>
    </ul>
    <a href="risk/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📉 Depreciation Calculator</h3>
    <p>Asset depreciation calculation tools.</p>
    <ul>
      <li>Straight-line depreciation</li>
      <li>Declining balance method</li>
      <li>Sum-of-years-digits</li>
      <li>Tax depreciation schedules</li>
    </ul>
    <a href="depreciation/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🏢 Business Analysis</h3>
    <p>Business analysis tools for financial planning.</p>
    <ul>
      <li>Break-even analysis</li>
      <li>Margin calculations</li>
      <li>Cost-volume-profit analysis</li>
      <li>Financial ratios</li>
    </ul>
    <a href="business/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🔧 Utility Calculator</h3>
    <p>Utility calculations for financial adjustments.</p>
    <ul>
      <li>Currency conversion</li>
      <li>Inflation adjustments</li>
      <li>Tax calculations</li>
      <li>Percentage calculations</li>
    </ul>
    <a href="utility/">Learn More →</a>
  </div>
</div>

## Getting Started

### Installation

```bash
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

### Basic Usage

All calculator modules are accessed through the main `CalculatorTools` class:

```python
from enhancedtoolkits import CalculatorTools

# Initialize calculator tools
calculator = CalculatorTools()

# Basic arithmetic
result = calculator.add(10, 5)
print(f"10 + 5 = {result}")

# Financial calculations
monthly_payment = calculator.calculate_loan_payment(
    principal=100000,
    annual_rate=0.05,
    years=30
)
print(f"Monthly payment: ${monthly_payment}")

# Investment analysis
npv = calculator.calculate_net_present_value(
    cash_flows=[-100000, 30000, 40000, 50000, 60000],
    discount_rate=0.10
)
print(f"NPV: ${npv}")
```

## Common Features

All calculator modules share these features:

### 🛡️ Input Validation
- Type checking and conversion
- Range validation
- Business rule validation
- Detailed error messages

### 📊 Comprehensive Results
- Detailed calculation breakdowns
- Multiple output formats
- Intermediate step results
- Summary statistics

### ⚡ Performance
- Optimized algorithms
- Efficient memory usage
- Fast computation
- Batch processing support

### 🔧 Integration
- Consistent API patterns
- JSON output format
- Error handling
- Logging and debugging

## Calculation Categories

### Basic Mathematics
- **Arithmetic**: Addition, subtraction, multiplication, division
- **Advanced Math**: Exponentiation, square root, factorial
- **Number Theory**: Prime checking, GCD, LCM

### Time Value of Money
- **Present Value**: Discount future cash flows
- **Future Value**: Compound present values
- **Annuities**: Regular payment streams
- **Perpetuities**: Infinite payment streams

### Investment Analysis
- **Valuation**: NPV, IRR, CAGR calculations
- **Performance**: ROI, profit margins
- **Comparison**: Investment ranking and selection

### Risk Assessment
- **Volatility**: Standard deviation, variance
- **Risk-Adjusted Returns**: Sharpe ratio, Treynor ratio
- **Portfolio Risk**: Beta, correlation analysis

### Debt Analysis
- **Loan Payments**: Monthly payment calculations
- **Amortization**: Payment schedules and breakdowns
- **Interest Analysis**: Total interest, payment timing

### Asset Management
- **Depreciation**: Multiple depreciation methods
- **Valuation**: Asset pricing and fair value
- **Tax Planning**: Depreciation tax benefits

## Example Workflows

### Investment Decision Analysis

```python
def analyze_investment_opportunity():
    calculator = CalculatorTools()
    
    # Calculate NPV
    cash_flows = [-100000, 25000, 30000, 35000, 40000, 45000]
    npv = calculator.calculate_net_present_value(
        cash_flows=cash_flows,
        discount_rate=0.12
    )
    
    # Calculate IRR
    irr = calculator.calculate_internal_rate_of_return(
        cash_flows=cash_flows
    )
    
    # Calculate payback period
    cumulative = 0
    payback_period = 0
    for i, cf in enumerate(cash_flows[1:], 1):
        cumulative += cf
        if cumulative >= abs(cash_flows[0]):
            payback_period = i
            break
    
    return {
        'npv': npv,
        'irr': irr,
        'payback_period': payback_period,
        'recommendation': 'Invest' if float(npv.split('$')[1].replace(',', '')) > 0 else 'Pass'
    }
```

### Loan Comparison

```python
def compare_loan_options():
    calculator = CalculatorTools()
    
    loan_options = [
        {'principal': 200000, 'rate': 0.035, 'years': 30},
        {'principal': 200000, 'rate': 0.040, 'years': 15},
        {'principal': 200000, 'rate': 0.045, 'years': 20}
    ]
    
    comparisons = []
    for i, loan in enumerate(loan_options, 1):
        payment = calculator.calculate_loan_payment(**loan)
        schedule = calculator.generate_amortization_schedule(**loan)
        
        # Parse results to get total interest
        import json
        schedule_data = json.loads(schedule)
        total_interest = sum(payment['interest'] for payment in schedule_data['payments'])
        
        comparisons.append({
            'option': i,
            'monthly_payment': payment,
            'total_interest': total_interest,
            'total_cost': loan['principal'] + total_interest
        })
    
    return comparisons
```

### Portfolio Risk Analysis

```python
def analyze_portfolio_risk():
    calculator = CalculatorTools()
    
    # Sample portfolio returns
    portfolio_returns = [0.12, -0.05, 0.18, 0.08, -0.02, 0.15, 0.10]
    market_returns = [0.10, -0.03, 0.15, 0.06, 0.01, 0.12, 0.08]
    risk_free_rate = 0.02
    
    # Calculate portfolio volatility
    volatility = calculator.calculate_volatility(portfolio_returns)
    
    # Calculate Sharpe ratio
    avg_return = sum(portfolio_returns) / len(portfolio_returns)
    sharpe = calculator.calculate_sharpe_ratio(
        returns=portfolio_returns,
        risk_free_rate=risk_free_rate
    )
    
    return {
        'average_return': avg_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe,
        'risk_assessment': 'High' if float(volatility.split('%')[0]) > 15 else 'Moderate'
    }
```

## Error Handling

All calculators include comprehensive error handling:

```python
try:
    result = calculator.calculate_loan_payment(
        principal=100000,
        annual_rate=0.05,
        years=30
    )
    print(result)
except ValueError as e:
    print(f"Input validation error: {e}")
except ZeroDivisionError as e:
    print(f"Mathematical error: {e}")
except Exception as e:
    print(f"Calculation error: {e}")
```

## Best Practices

1. **Validate Inputs**: Always check input parameters before calculations
2. **Handle Edge Cases**: Consider zero values, negative numbers, and extremes
3. **Use Appropriate Precision**: Choose decimal places based on use case
4. **Document Assumptions**: Clearly state calculation assumptions
5. **Test Results**: Verify calculations with known examples

## Performance Tips

- Use batch calculations for multiple scenarios
- Cache frequently used calculations
- Choose appropriate data types for precision needs
- Consider memory usage for large datasets

## Next Steps

1. **Choose a calculator module** that fits your needs
2. **Read the specific documentation** for detailed usage examples
3. **Try the calculation examples** provided in each module
4. **Integrate with other toolkits** for comprehensive analysis

## Related Tools

- [Finance Tools](../toolkits/finance.md) - Real-time financial data
- [Reasoning Tools](../toolkits/reasoning.md) - Decision analysis
- [Thinking Tools](../toolkits/thinking.md) - Structured analysis

## Need Help?

- 📖 Check individual calculator documentation
- 🔧 Learn about [Advanced Features](../advanced/)
- 💬 Join our [community discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions)