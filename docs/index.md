# Enhanced Toolkits for AI Agents

Production-ready AI agent tools with **OpenAI-compatible tool calling** and first-class support for the **Agno** framework.

Enhanced Toolkits provides:

- **9 core toolkits** (reasoning, search, thinking, files, finance, youtube, weather, url downloading, orchestration/planning)
- **9 calculator modules** under `enhancedtoolkits.calculators`

## 🚀 Quick Start (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    WeatherTools,
    DownloadingTools,
)

agent = Agent(
    name="AI Assistant",
    model="gpt-4",
    tools=[
        ReasoningTools(),
        SearxngTools(host="http://searxng:8080"),
        ThinkingTools(),
        FilesTools(base_dir="/app/workspace"),
        YFinanceTools(),
        YouTubeTools(),
        WeatherTools(),
        DownloadingTools(),
    ],
)
```

## 🧮 Calculator Modules

Calculator tools are separate classes. Example:

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
)

agent = Agent(
    name="Calculator Agent",
    model="gpt-4",
    tools=[ArithmeticCalculatorTools(), TimeValueCalculatorTools()],
)
```

## Documentation

- Core toolkits: [`docs/toolkits/index.md`](toolkits/index.md)
- Calculator modules: [`docs/calculators/index.md`](calculators/index.md)
- API reference: [`docs/api/index.md`](api/index.md)
- Getting started: [`docs/getting-started/index.md`](getting-started/index.md)

## Strict schemas

All toolkits build on [`StrictToolkit`](api/base.md), which enforces strict tool schemas for agent reliability.
