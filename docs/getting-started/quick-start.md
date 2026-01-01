# Quick Start

This guide shows how to use Enhanced Toolkits in Python.

> Most users should install `enhancedtoolkits[full]` to ensure optional toolkit dependencies are present.

## Core toolkits (direct usage)

```python
import json

from enhancedtoolkits import ReasoningTools, YFinanceTools

reasoning = ReasoningTools()
finance = YFinanceTools()

# Fetch current stock price
price_json = finance.fetch_current_stock_price("AAPL")
price = json.loads(price_json)

# Add a reasoning step (requires an agent/team object to store session state)
# If you are not using Agno yet, any object with attributes works.
class Session:  # minimal state container
    pass

agent = Session()

reasoning.add_structured_reasoning_step(
    agent_or_team=agent,
    problem=f"Should we look deeper into AAPL? Current price: {price.get('current_price')}",
    cognitive_mode="analysis",
    reasoning_type="inductive",
    evidence=["We have a current price snapshot", "Need fundamentals and risk view"],
    confidence=0.6,
)

# Synthesize a conclusion
print(
    reasoning.synthesize_reasoning_chain_into_conclusion_or_insight(
        agent_or_team=agent,
        synthesis_type="conclusion",
    )
)
```

## Calculator modules

Calculator modules are separate toolkits under `enhancedtoolkits.calculators`.

```python
import json

from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
    LoanCalculatorTools,
)

arith = ArithmeticCalculatorTools()
tv = TimeValueCalculatorTools()
loan = LoanCalculatorTools()

# Add numbers
print(arith.add(10, 5))

# Future value
fv_json = tv.calculate_future_value(present_value=10000, rate=0.07, periods=10)
print(json.loads(fv_json))

# Loan payment (generic: principal, periodic rate, number of periods)
payment_json = loan.calculate_loan_payment(principal=100000, rate=0.05 / 12, periods=360)
print(json.loads(payment_json))
```

## Using with Agno

```python
from agno.agent import Agent
from enhancedtoolkits import ReasoningTools, YFinanceTools

agent = Agent(
    name="Analyst",
    model="gpt-4",
    tools=[ReasoningTools(), YFinanceTools()],
)

# The agent can now call tool functions via tool calling.
```

## Next Steps

- Core toolkits overview: [`docs/toolkits/index.md`](../toolkits/index.md)
- Calculator modules: [`docs/calculators/index.md`](../calculators/index.md)
- Configuration: [`docs/getting-started/configuration.md`](configuration.md)
