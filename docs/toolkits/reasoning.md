# Reasoning Tools

The [`ReasoningTools`](../api/reasoning.md) toolkit provides **text-first reasoning utilities** for AI agents:

- Build a compact reasoning chain (steps + reflections + scratchpad)
- Optionally detect simple bias markers in text
- Assess chain quality and suggest improvements
- Synthesize the chain into a short conclusion/summary/insight

All public functions return **strings** (human-readable, markdown-ish).

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import ReasoningTools

agent = Agent(
    name="Analyst",
    model="gpt-4",
    tools=[ReasoningTools(reasoning_depth=5, enable_bias_detection=True)],
)
```

> The `agent_or_team` parameter should be your agent/team object (it is used as the session state container).

## 🔧 Key Concepts

### Valid values

- `cognitive_mode`: `analysis | synthesis | evaluation | planning | creative | reflection`
- `reasoning_type`: `deductive | inductive | abductive | causal | probabilistic | analogical`
- `synthesis_type`: `conclusion | summary | insights`
- scratchpad `operation`: `set | get | list | clear`

## 🧠 Available Functions

### `add_structured_reasoning_step(agent_or_team, problem, cognitive_mode='analysis', reasoning_type='deductive', evidence=None, confidence=0.5)`
Adds a numbered reasoning step and (optionally) records evidence and bias markers.

### `add_meta_cognitive_reflection(agent_or_team, reflection, step_id=None)`
Adds a reflection entry for the current reasoning chain.

### `manage_working_memory_scratchpad(agent_or_team, key, value=None, operation='set')`
Simple key/value scratchpad:
- `set`: set `key=value`
- `get`: retrieve one key
- `list`: list all keys
- `clear`: clear one key or all keys (`key='all'`)

### `assess_reasoning_quality_and_suggest_improvements(agent_or_team)`
Computes a compact quality score and suggests improvements.

### `synthesize_reasoning_chain_into_conclusion_or_insight(agent_or_team, synthesis_type='conclusion')`
Produces a short synthesis and marks the chain as completed.

### `retrieve_current_reasoning_session_state(agent_or_team)`
Returns a compact summary of the current chain state.

### `reset_reasoning_session_state(agent_or_team)`
Clears the current reasoning session.

## ✅ Example Workflow

```python
from enhancedtoolkits import ReasoningTools

reasoning = ReasoningTools()

# 1) Add a step
reasoning.add_structured_reasoning_step(
    agent_or_team=agent,
    problem="Should we invest in renewable energy stocks?",
    cognitive_mode="analysis",
    reasoning_type="inductive",
    evidence=["Costs are declining", "Policy incentives are rising"],
    confidence=0.6,
)

# 2) Add a reflection
reasoning.add_meta_cognitive_reflection(
    agent_or_team=agent,
    reflection="We may be overweighting recent headlines; check longer-term fundamentals.",
    step_id=1,
)

# 3) Store something in scratchpad
reasoning.manage_working_memory_scratchpad(
    agent_or_team=agent,
    key="tickers",
    value="ICLN,TAN",
    operation="set",
)

# 4) Assess quality
reasoning.assess_reasoning_quality_and_suggest_improvements(agent_or_team=agent)

# 5) Synthesize
reasoning.synthesize_reasoning_chain_into_conclusion_or_insight(
    agent_or_team=agent,
    synthesis_type="conclusion",
)

# 6) Reset
reasoning.reset_reasoning_session_state(agent_or_team=agent)
```

## 📝 Notes / Best Practices

- Keep each step short (1–3 sentences). Store bulky details in `evidence` or scratchpad keys.
- Prefer synthesis outputs instead of returning the entire chain verbatim.

## API Reference

- [`docs/api/reasoning.md`](../api/reasoning.md)
