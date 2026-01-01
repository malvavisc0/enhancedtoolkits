# Thinking Tools

The [`ThinkingTools`](../api/thinking.md) toolkit provides a **text-first thinking/journaling chain** for agents:

- Build a step-by-step chain
- Add meta-cognitive reflections
- Store intermediate data in a scratchpad
- Synthesize the chain into a compact output

All public functions return **strings** (human-readable, markdown-ish).

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import ThinkingTools

agent = Agent(
    name="Planner",
    model="gpt-4",
    tools=[ThinkingTools(max_chain_length=10, confidence_threshold=0.7)],
)
```

> The `agent` parameter is used as the session state container.

## 🔧 Valid values

- `thinking_type`: `analysis | synthesis | evaluation | planning | creative | reflection`
- `synthesis_type`: `conclusion | summary | insights | next_steps`
- scratchpad `operation`: `set | get | list | clear`

## 🧠 Available Functions

### `build_step_by_step_reasoning_chain(agent, problem, thinking_type='analysis', context=None, evidence=None, confidence=0.5)`
Starts a chain (first call) or appends a step (subsequent calls).

### `add_meta_cognitive_reflection(agent, reflection, step_id=None)`
Adds a reflection entry for the current chain.

### `manage_working_memory_scratchpad(agent, key, value=None, operation='set')`
Scratchpad operations:
- `set`: set `key=value`
- `get`: retrieve one key
- `list`: list all keys
- `clear`: clear one key or all keys (`key='all'`)

### `assess_reasoning_chain_quality_and_suggest_improvements(agent)`
Computes a compact quality score and suggests improvements.

### `synthesize_reasoning_chain_into_output(agent, synthesis_type='conclusion')`
Returns a short synthesis and closes the current chain.

### `retrieve_current_thinking_chain_state(agent)`
Returns a compact state summary.

### `reset_current_thinking_chain(agent)`
Clears the current chain (does not delete history summaries).

## ✅ Example Workflow

```python
from enhancedtoolkits import ThinkingTools

thinking = ThinkingTools()

# 1) Start a chain
thinking.build_step_by_step_reasoning_chain(
    agent=agent,
    problem="Plan a 2-week study schedule for system design interviews",
    thinking_type="planning",
    context="I can study 90 minutes per weekday and 3h on weekends",
    confidence=0.6,
)

# 2) Add another step
thinking.build_step_by_step_reasoning_chain(
    agent=agent,
    problem="Week 1: focus on scalability fundamentals + 2 mock designs",
    thinking_type="planning",
    confidence=0.7,
)

# 3) Add a reflection
thinking.add_meta_cognitive_reflection(
    agent=agent,
    reflection="Risk: underestimating review time; schedule buffer slots.",
)

# 4) Synthesize into next steps
thinking.synthesize_reasoning_chain_into_output(
    agent=agent,
    synthesis_type="next_steps",
)
```

## API Reference

- [`docs/api/thinking.md`](../api/thinking.md)
