# Thinking Tools for AI Agents

The Thinking Tools provide structured cognitive frameworks for systematic problem analysis and decision-making in AI agents.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import ThinkingTools

# Initialize for your AI agent
thinking = ThinkingTools(
    enable_bias_detection=True,      # Detect cognitive biases
    enable_quality_assessment=True,  # Assess thinking quality
    thinking_depth=3                 # Analysis depth level
)

# Register with your agent
agent.register_tools([thinking])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_bias_detection` | bool | `True` | Detect cognitive biases in thinking |
| `enable_quality_assessment` | bool | `True` | Assess thinking depth and clarity |
| `thinking_depth` | int | `3` | Maximum depth of analysis |
| `instructions` | str | `None` | Custom thinking instructions |

## 🧠 Available Functions

Your AI agent will have access to these functions:

### `think()`
Process thoughts using structured cognitive frameworks.

**Parameters:**
- `agent_or_team`: Agent instance for session tracking
- `thought`: The thought or problem to analyze
- `thinking_type`: Type of thinking framework to apply
- `context`: Additional context for analysis

**Thinking Types:**
- `"analysis"` - Systematic breakdown and examination
- `"synthesis"` - Combining elements into coherent whole
- `"evaluation"` - Critical assessment and judgment
- `"reflection"` - Self-examination and metacognition
- `"planning"` - Strategic planning and goal setting
- `"problem_solving"` - Systematic problem resolution
- `"creative"` - Creative and innovative thinking
- `"critical"` - Critical analysis and reasoning

### `analyze_thinking_quality()`
Assess the quality of thinking processes.

### `detect_thinking_biases()`
Identify cognitive biases in thinking patterns.

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import ThinkingTools

thinking = ThinkingTools()

# Get function schema for OpenAI
tools = [thinking.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Analyze the pros and cons of remote work"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import ThinkingTools

agent = Agent(
    name="Strategic Analyst",
    model="gpt-4",
    tools=[ThinkingTools(thinking_depth=5)]
)

# Agent can now use thinking functions
response = agent.run("Think through the strategic implications of AI adoption")
```

## 🔧 Production Configuration

### Basic Setup
```python
thinking = ThinkingTools()
```

### Advanced Setup
```python
thinking = ThinkingTools(
    enable_bias_detection=True,
    enable_quality_assessment=True,
    thinking_depth=5,
    instructions="Focus on strategic and long-term implications"
)
```

### Environment Variables
```bash
# Optional: Set logging level
LOG_LEVEL=INFO
```

## 🛡️ Features

- **8 Thinking Types**: Analysis, synthesis, evaluation, reflection, planning, problem-solving, creative, critical
- **Bias Detection**: Automatic identification of cognitive biases
- **Quality Assessment**: Depth, clarity, and evidence integration analysis
- **Session Tracking**: Maintains thinking patterns and progression
- **Structured Output**: Consistent, analyzable thinking results

## 🔍 Example Agent Interactions

**Agent Query:** "Think through the decision to expand into international markets"

**Thinking Tool Response:**
```json
{
  "thinking_type": "analysis",
  "analysis": {
    "factors": ["Market size", "Competition", "Regulatory environment"],
    "considerations": ["Cultural differences", "Currency risks", "Local partnerships"],
    "framework": "Systematic market analysis"
  },
  "quality_assessment": {
    "depth": "High",
    "clarity": "Clear",
    "evidence_integration": "Good"
  },
  "detected_biases": [],
  "recommendations": ["Conduct market research", "Assess regulatory requirements"]
}
```

## 📊 Monitoring

Enable detailed logging to monitor thinking processes:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

thinking = ThinkingTools(debug=True)
```

## 🚀 Next Steps

1. **Initialize** ThinkingTools with your preferred configuration
2. **Register** with your AI agent framework
3. **Test** with sample thinking queries
4. **Monitor** thinking quality and bias detection
5. **Adjust** thinking depth and bias detection as needed

The Thinking Tools help your AI agent develop more structured, unbiased, and high-quality thought processes for complex decision-making scenarios.