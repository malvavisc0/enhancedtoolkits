# Arithmetic Calculator

The [`ArithmeticCalculatorTools`](../api/calculators/arithmetic.md) module provides basic arithmetic and small statistics utilities.

All functions return **JSON strings**.

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import ArithmeticCalculatorTools

agent = Agent(
    name="Math Helper",
    model="gpt-4",
    tools=[ArithmeticCalculatorTools()],
)
```

## 🔢 Common Functions

Core operations:

- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`
- `exponentiate(a, b)`
- `square_root(n)`
- `factorial(n)`
- `is_prime(n)`

Additional utilities include:

- `modulo(a, b)`, `absolute(n)`, `round_number(n, decimals=0)`
- `log(n, base=10.0)`, `ln(n)`
- `gcd(a, b)`, `lcm(a, b)`
- `mean(numbers)`, `median(numbers)`, `standard_deviation(numbers)`

## ✅ Examples

```python
import json
from enhancedtoolkits.calculators import ArithmeticCalculatorTools

calc = ArithmeticCalculatorTools()

add_json = calc.add(10, 5)
print(json.loads(add_json)["result"])  # 15

sqrt_json = calc.square_root(16)
print(json.loads(sqrt_json)["result"])  # 4
```

## API Reference

- [`docs/api/calculators/arithmetic.md`](../api/calculators/arithmetic.md)
