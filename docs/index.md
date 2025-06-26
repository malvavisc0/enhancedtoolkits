# Enhanced Toolkits for AI Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/malvavisc0/enhancedtoolkits/refs/heads/main/LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno Framework](https://img.shields.io/badge/framework-Agno-green.svg)](https://github.com/agno-ai/agno)

**Production-ready AI agent tools with OpenAI function calling compatibility.**

Enhanced Toolkits provides **8 core toolkits** and **9 calculator modules** designed specifically for AI agents that need reliable, robust capabilities with enterprise-grade error handling and validation.

## 🤖 For AI Agent Developers

These tools are designed to be **registered with AI agents** using the OpenAI function calling API or the Agno framework. Each tool provides:

- ✅ **OpenAI Compatible** function schemas
- ✅ **Strict parameter validation** for reliable agent execution
- ✅ **Comprehensive error handling** with detailed responses
- ✅ **Production-ready** caching and rate limiting
- ✅ **Enterprise security** controls and validation

## 🚀 Quick Start for AI Agents

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
    DownloaderTools
)

# Create agent with tools (Agno automatically handles registration)
agent = Agent(
    name="AI Assistant",
    model="gpt-4",
    tools=[
        ReasoningTools(),
        SearxngTools(host="http://searxng:8080"),
        ThinkingTools(),
        FilesTools(),
        YFinanceTools(),
        YouTubeTools(),
        WeatherTools(),
        DownloaderTools()
    ]
)
```

## 🛠️ Available Tools

### Core Toolkits (8 Tools)

<div class="toolkit-grid">
  <div class="toolkit-card">
    <h3>🧠 Reasoning Tools</h3>
    <p>Multi-modal reasoning with cognitive bias detection for complex decision making.</p>
    <a href="toolkits/reasoning.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🔍 Search Tools</h3>
    <p>Web search with content extraction using SearxNG integration.</p>
    <a href="toolkits/searxng.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>💭 Thinking Tools</h3>
    <p>Structured cognitive frameworks for systematic problem analysis.</p>
    <a href="toolkits/thinking.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📁 Files Tools</h3>
    <p>Enterprise-grade file operations with comprehensive security controls.</p>
    <a href="toolkits/files.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📈 Finance Tools</h3>
    <p>Real-time financial data and market information via Yahoo Finance.</p>
    <a href="toolkits/finance.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🎥 YouTube Tools</h3>
    <p>Video metadata and transcript extraction with multi-language support.</p>
    <a href="toolkits/youtube.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>☁️ Weather Tools</h3>
    <p>Weather data and forecasts with support for 30+ languages.</p>
    <a href="toolkits/weather.md">Setup Guide →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📥 Downloader Tools</h3>
    <p>Universal file downloading with anti-bot bypass capabilities.</p>
    <a href="toolkits/downloader.md">Setup Guide →</a>
  </div>
</div>

### Calculator Modules (9 Calculators)

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

# Create agent with calculator tools
agent = Agent(
    name="Financial Analyst",
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

[View all calculator modules →](calculators/index.md)

## 🏗️ AI Agent Integration

### OpenAI Function Calling

```python
import openai
from enhancedtoolkits import ReasoningTools, YFinanceTools

# Initialize tools
reasoning = ReasoningTools()
finance = YFinanceTools()

# Get OpenAI-compatible function schemas
tools = [
    reasoning.get_openai_schema(),
    finance.get_openai_schema()
]

# Use with OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Analyze AAPL stock"}],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework Integration

```python
from agno.agent import Agent
from enhancedtoolkits import *

# Create agent with tools (Agno handles everything automatically)
agent = Agent(
    name="Financial Analyst",
    model="gpt-4",
    tools=[
        ReasoningTools(),
        YFinanceTools(),
        ArithmeticCalculatorTools(),
        InvestmentAnalysisCalculatorTools()
    ]
)

# Agent automatically has access to all tool functions
response = agent.run("Analyze the investment potential of AAPL")
```

## 🛡️ Why StrictToolkit?

All tools inherit from **StrictToolkit**, which ensures:

- **All parameters are required** in function schemas (no optional parameters that confuse agents)
- **Consistent error handling** across all tools
- **OpenAI compatibility** out of the box
- **Reliable agent execution** with predictable behavior

## 📦 Installation

```bash
# Install with core dependencies
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git

# Install with all optional dependencies (recommended)
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

## 🔧 Configuration

Most tools support configuration for production use:

```python
# Example: Configure tools for production
reasoning = ReasoningTools(
    reasoning_depth=5,
    enable_bias_detection=True
)

finance = YFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)

search = SearxngTools(
    host="http://your-searxng:8080",
    max_results=10,
    enable_content_fetching=True
)
```

## 📚 Documentation Sections

- **[Getting Started](getting-started/index.md)** - Installation and setup for AI agents
- **[Core Toolkits](toolkits/index.md)** - Setup guides for all 8 core tools
- **[Calculator Modules](calculators/index.md)** - Setup guides for all 9 calculator tools
- **[API Reference](api/index.md)** - Complete function schemas and parameters
- **[Developer Guide](developer/index.md)** - Contributing and deployment

## 🎯 Next Steps

1. **[Install Enhanced Toolkits](getting-started/installation.md)**
2. **[Choose your tools](toolkits/index.md)** from the 8 core toolkits
3. **[Add calculators](calculators/index.md)** from the 9 available modules
4. **[Register with your agent](getting-started/quick-start.md)** using OpenAI or Agno
5. **[Configure for production](getting-started/configuration.md)** with caching and rate limiting

---

**Built for AI agent developers who need reliable, production-ready tools.** 🤖