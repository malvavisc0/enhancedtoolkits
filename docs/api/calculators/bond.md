# Bond Calculator API Reference

API documentation for the Bond Calculator - bond valuation, yield calculations, and fixed-income analysis tools.

## Class: BondCalculatorTools

Bond calculation toolkit providing comprehensive tools for bond valuation, yield analysis, and fixed-income investment calculations.

### BondCalculatorTools()

Initialize the Bond Calculator toolkit.

### Methods

#### calculate_bond_price()

Calculate the current price of a bond based on yield and characteristics.

**Parameters:**
- `face_value` (float): Bond face value (par value)
- `coupon_rate` (float): Annual coupon rate percentage
- `yield_to_maturity` (float): Required yield to maturity percentage
- `years_to_maturity` (float): Years until bond maturity
- `payment_frequency` (int): Coupon payments per year (1, 2, 4, 12)

**Returns:**
- `dict`: Bond price calculation with premium/discount analysis

#### calculate_bond_yield()

Calculate yield to maturity and current yield for a bond.

**Parameters:**
- `current_price` (float): Current market price of the bond
- `face_value` (float): Bond face value (par value)
- `coupon_rate` (float): Annual coupon rate percentage
- `years_to_maturity` (float): Years until bond maturity
- `payment_frequency` (int): Coupon payments per year

**Returns:**
- `dict`: Yield calculations including YTM and current yield

#### calculate_duration()

Calculate Macaulay duration and modified duration for interest rate sensitivity.

**Parameters:**
- `face_value` (float): Bond face value
- `coupon_rate` (float): Annual coupon rate percentage
- `yield_to_maturity` (float): Yield to maturity percentage
- `years_to_maturity` (float): Years until maturity
- `payment_frequency` (int): Coupon payments per year

**Returns:**
- `dict`: Duration calculations for interest rate risk assessment

#### calculate_convexity()

Calculate bond convexity for advanced interest rate risk analysis.

**Parameters:**
- `face_value` (float): Bond face value
- `coupon_rate` (float): Annual coupon rate percentage
- `yield_to_maturity` (float): Yield to maturity percentage
- `years_to_maturity` (float): Years until maturity
- `payment_frequency` (int): Coupon payments per year

**Returns:**
- `dict`: Convexity calculation for price sensitivity analysis

#### calculate_accrued_interest()

Calculate accrued interest for bond trading between coupon dates.

**Parameters:**
- `face_value` (float): Bond face value
- `coupon_rate` (float): Annual coupon rate percentage
- `days_since_last_coupon` (int): Days since last coupon payment
- `days_in_coupon_period` (int): Total days in coupon period

**Returns:**
- `dict`: Accrued interest calculation for settlement

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import BondCalculatorTools

agent = Agent(
    name="Bond Analyst",
    model="gpt-4",
    tools=[BondCalculatorTools()]
)
```

## Bond Metrics

### Valuation
- **Bond Price**: Present value of future cash flows
- **Yield to Maturity**: Internal rate of return
- **Current Yield**: Annual coupon divided by current price

### Risk Measures
- **Duration**: Price sensitivity to interest rate changes
- **Convexity**: Curvature of price-yield relationship
- **Credit Risk**: Default probability assessment

## Related Documentation

- [Bond Calculator Guide](../../calculators/bond.md)
- [Investment Calculator API](investment.md)
- [Risk Metrics Calculator API](risk.md)