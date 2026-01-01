# Orchestration & Planning Tools

The orchestration toolkit provides a **plan + task graph** (dependencies) that helps an agent coordinate multi-step work.

It is designed to be:

- **Deterministic and auditable** (no hidden planning logic)
- **Dependency-aware** (`depends_on`)
- **Tool-call friendly** (returns **JSON strings**)

## Auto-loaded when using any toolkit

`enhancedtoolkits` auto-loads the orchestration singleton and **injects orchestration functions into every toolkit** via [`StrictToolkit`](../api/base.md).

That means:

- If you add *any* toolkit (e.g. `ReasoningTools`) to your agent, you also get these orchestration tools.
- Injected tool names are **prefixed** to avoid collisions:
  - `orchestrator_create_plan()`
  - `orchestrator_add_task()`
  - `orchestrator_update_task_status()`
  - `orchestrator_next_actions()`
  - `orchestrator_summarize_progress()`
  - `orchestrator_reset_plan()`

## Optional: add the toolkit directly

You can also add [`OrchestrationTools`](../api/orchestration.md) directly to your agent. In that case, the tool names are the “clean” names:

- `create_plan()`
- `add_task()`
- `update_task_status()`
- `next_actions()`
- `summarize_progress()`
- `reset_plan()`

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import ReasoningTools

# Orchestration tools are auto-injected into every toolkit instance.
agent = Agent(
    name="Planner",
    model="gpt-4",
    tools=[ReasoningTools()],
)
```

## ✅ Example workflow

```python
import json

class Session:
    pass

agent = Session()

# create a plan
plan_json = ReasoningTools().orchestrator.create_plan(
    agent_or_team=agent,
    goal="Write docs + run validation",
    tasks=[
        {"title": "Update docs", "priority": 5},
        {"title": "Run link checks", "priority": 3, "depends_on": [1]},
    ],
)
print(json.loads(plan_json)["plan"]["plan_id"])

# ask for next task(s)
actions_json = ReasoningTools().orchestrator.next_actions(agent_or_team=agent, max_actions=1)
print(json.loads(actions_json)["actions"])

# mark done
ReasoningTools().orchestrator.update_task_status(agent_or_team=agent, task_id=1, status="done")

# summarize
print(ReasoningTools().orchestrator.summarize_progress(agent_or_team=agent))
```

## API Reference

- [`docs/api/orchestration.md`](../api/orchestration.md)
