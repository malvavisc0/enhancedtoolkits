# Arithmetic Calculator

The Arithmetic Calculator provides basic mathematical operations with comprehensive validation and error handling.

## Overview

The `ArithmeticCalculatorTools` class offers fundamental arithmetic operations that form the foundation for more complex financial calculations. All operations include input validation, type checking, and detailed error handling.

## Available Methods

### Basic Operations

#### `add(a, b)`
Add two numbers together.

```python
from enhancedtoolkits import CalculatorTools

calculator = CalculatorTools()
result = calculator.add(10, 5)
print(result)  # "15"
```

#### `subtract(a, b)`
Subtract the second number from the first.

```python
result = calculator.subtract(10, 3)
print(result)  # "7"
```

#### `multiply(a, b)`
Multiply two numbers.

```python
result = calculator.multiply(6, 7)
print(result)  # "42"
```

#### `divide(a, b)`
Divide the first number by the second.

```python
result = calculator.divide(15, 3)
print(result)  # "5"

# Handles division by zero
try:
    result = calculator.divide(10, 0)
except ZeroDivisionError as e:
    print(f"Error: {e}")
```

### Advanced Operations

#### `exponentiate(base, exponent)`
Raise a number to a power.

```python
result = calculator.exponentiate(2, 8)
print(result)  # "256"

# Supports fractional exponents
result = calculator.exponentiate(9, 0.5)
print(result)  # "3" (square root of 9)
```

#### `square_root(number)`
Calculate the square root of a number.

```python
result = calculator.square_root(16)
print(result)  # "4"

# Handles negative numbers
try:
    result = calculator.square_root(-4)
except ValueError as e:
    print(f"Error: {e}")
```

#### `factorial(n)`
Calculate the factorial of a non-negative integer.

```python
result = calculator.factorial(5)
print(result)  # "120" (5! = 5×4×3×2×1)

result = calculator.factorial(0)
print(result)  # "1" (0! = 1 by definition)
```

#### `is_prime(number)`
Check if a number is prime.

```python
result = calculator.is_prime(17)
print(result)  # "true"

result = calculator.is_prime(15)
print(result)  # "false"
```

## Input Validation

All methods include comprehensive input validation:

### Type Validation
```python
# Automatically converts compatible types
result = calculator.add("10", 5)    # Works: converts "10" to 10
result = calculator.add(10.5, 5)    # Works: handles floats

# Rejects invalid types
try:
    result = calculator.add("abc", 5)
except ValueError as e:
    print(f"Invalid input: {e}")
```

### Range Validation
```python
# Factorial only accepts non-negative integers
try:
    result = calculator.factorial(-5)
except ValueError as e:
    print(f"Invalid range: {e}")

# Square root only accepts non-negative numbers
try:
    result = calculator.square_root(-16)
except ValueError as e:
    print(f"Invalid range: {e}")
```

## Practical Examples

### Basic Calculator Function

```python
def basic_calculator():
    calculator = CalculatorTools()
    
    print("Basic Calculator Examples:")
    
    # Basic operations
    print(f"Addition: 15 + 25 = {calculator.add(15, 25)}")
    print(f"Subtraction: 50 - 18 = {calculator.subtract(50, 18)}")
    print(f"Multiplication: 7 × 8 = {calculator.multiply(7, 8)}")
    print(f"Division: 84 ÷ 12 = {calculator.divide(84, 12)}")
    
    # Advanced operations
    print(f"Exponentiation: 3^4 = {calculator.exponentiate(3, 4)}")
    print(f"Square root: √64 = {calculator.square_root(64)}")
    print(f"Factorial: 6! = {calculator.factorial(6)}")
    
    # Prime checking
    numbers_to_check = [2, 3, 4, 17, 25, 29]
    for num in numbers_to_check:
        is_prime = calculator.is_prime(num)
        print(f"{num} is {'prime' if is_prime == 'true' else 'not prime'}")

basic_calculator()
```

### Mathematical Sequence Generator

```python
def generate_sequences():
    calculator = CalculatorTools()
    
    # Generate factorial sequence
    print("Factorial sequence:")
    for i in range(8):
        factorial = calculator.factorial(i)
        print(f"{i}! = {factorial}")
    
    # Generate perfect squares
    print("\nPerfect squares:")
    for i in range(1, 11):
        square = calculator.exponentiate(i, 2)
        print(f"{i}² = {square}")
    
    # Find prime numbers up to 30
    print("\nPrime numbers up to 30:")
    primes = []
    for i in range(2, 31):
        if calculator.is_prime(i) == "true":
            primes.append(i)
    print(f"Primes: {primes}")

generate_sequences()
```

### Compound Interest Calculator

```python
def compound_interest_calculator():
    calculator = CalculatorTools()
    
    principal = 1000  # Initial amount
    rate = 0.05       # 5% annual interest
    years = 10        # Investment period
    
    print(f"Compound Interest Calculation:")
    print(f"Principal: ${principal}")
    print(f"Annual Rate: {rate * 100}%")
    print(f"Years: {years}")
    print()
    
    # Calculate year by year
    current_amount = principal
    for year in range(1, years + 1):
        # A = P(1 + r)^t
        growth_factor = calculator.add(1, rate)
        amount = calculator.multiply(
            principal,
            calculator.exponentiate(growth_factor, year)
        )
        
        yearly_growth = calculator.subtract(amount, current_amount)
        current_amount = amount
        
        print(f"Year {year}: ${float(amount):.2f} (Growth: ${float(yearly_growth):.2f})")
    
    total_growth = calculator.subtract(current_amount, principal)
    print(f"\nTotal Growth: ${float(total_growth):.2f}")

compound_interest_calculator()
```

## Error Handling

The arithmetic calculator includes comprehensive error handling:

```python
def safe_calculation_example():
    calculator = CalculatorTools()
    
    operations = [
        ("add", [10, 5]),
        ("divide", [10, 0]),        # Division by zero
        ("square_root", [-4]),      # Negative square root
        ("factorial", [-1]),        # Negative factorial
        ("is_prime", [1.5])        # Non-integer for prime check
    ]
    
    for operation, args in operations:
        try:
            method = getattr(calculator, operation)
            result = method(*args)
            print(f"{operation}({', '.join(map(str, args))}) = {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"{operation}({', '.join(map(str, args))}) failed: {e}")

safe_calculation_example()
```

## Performance Considerations

### Large Number Handling
```python
# Factorial grows very quickly
calculator = CalculatorTools()

# This works fine
result = calculator.factorial(10)  # 3,628,800

# This might be slow for very large numbers
result = calculator.factorial(100)  # Very large number

# Prime checking can be slow for large numbers
result = calculator.is_prime(982451653)  # Takes time for large primes
```

### Precision Considerations
```python
# Floating point precision
result = calculator.divide(1, 3)
print(result)  # May show "0.3333333333333333"

# For financial calculations, consider rounding
amount = float(calculator.divide(100, 3))
rounded_amount = round(amount, 2)
print(f"${rounded_amount}")  # $33.33
```

## Integration with Other Calculators

The arithmetic calculator forms the foundation for other calculator modules:

```python
# Used internally by financial calculators
def manual_loan_payment():
    calculator = CalculatorTools()
    
    principal = 100000
    monthly_rate = 0.05 / 12  # 5% annual rate, monthly
    months = 30 * 12          # 30 years
    
    # Manual PMT calculation using arithmetic operations
    # PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
    
    one_plus_r = calculator.add(1, monthly_rate)
    power_term = calculator.exponentiate(one_plus_r, months)
    numerator = calculator.multiply(
        principal,
        calculator.multiply(monthly_rate, power_term)
    )
    denominator = calculator.subtract(power_term, 1)
    payment = calculator.divide(numerator, denominator)
    
    print(f"Monthly payment: ${float(payment):.2f}")

manual_loan_payment()
```

## Best Practices

1. **Input Validation**: Always validate inputs before calculations
2. **Error Handling**: Use try-catch blocks for operations that might fail
3. **Type Conversion**: Be explicit about number types when precision matters
4. **Range Checking**: Verify inputs are within valid ranges
5. **Result Formatting**: Format results appropriately for display

## Common Use Cases

- **Basic calculations** in financial applications
- **Input validation** for other calculator modules
- **Mathematical sequence generation**
- **Educational tools** for teaching mathematics
- **Data preprocessing** for financial analysis

## Related Calculators

- [Time Value Calculator](time-value.md) - Uses arithmetic for compound interest
- [Investment Analysis](investment.md) - Uses arithmetic for NPV/IRR calculations
- [Loan Calculator](loan.md) - Uses arithmetic for payment calculations

## API Reference

For complete method signatures and parameters, see the [API Reference](../api/calculators/arithmetic.md).
