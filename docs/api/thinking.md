# Thinking Tools API Reference

API documentation for the Thinking Tools toolkit - structured cognitive frameworks for systematic problem analysis.

## Class: ThinkingTools

Structured cognitive frameworks toolkit for systematic problem analysis and creative thinking methodologies.

### ThinkingTools()

Initialize the Thinking Tools toolkit.

**Parameters:**
- `enable_caching` (bool, optional): Enable response caching. Default: True
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: 300
- `timeout` (int, optional): Request timeout in seconds. Default: 30

### Methods

#### think_step_by_step()

Apply step-by-step thinking methodology to break down complex problems.

**Parameters:**
- `agent_or_team` (Agent): The agent or team to use for thinking
- `problem` (str): The problem to analyze step by step
- `steps` (int): Number of thinking steps to perform
- `context` (str, optional): Additional context for the problem

**Returns:**
- `dict`: Structured step-by-step analysis with reasoning chain

#### apply_first_principles()

Apply first principles thinking to break down problems to fundamental truths.

**Parameters:**
- `agent_or_team` (Agent): The agent or team to use for analysis
- `problem` (str): The problem to analyze using first principles
- `assumptions` (List[str]): Current assumptions to challenge
- `depth` (int): Depth of first principles analysis

**Returns:**
- `dict`: First principles breakdown with fundamental insights

#### use_systems_thinking()

Apply systems thinking to understand interconnections and relationships.

**Parameters:**
- `agent_or_team` (Agent): The agent or team to use for analysis
- `system` (str): The system to analyze
- `components` (List[str]): System components to consider
- `relationships` (List[str]): Known relationships between components

**Returns:**
- `dict`: Systems analysis with component interactions and feedback loops

#### apply_lateral_thinking()

Use lateral thinking techniques to generate creative solutions.

**Parameters:**
- `agent_or_team` (Agent): The agent or team to use for creative thinking
- `problem` (str): The problem requiring creative solutions
- `constraints` (List[str]): Current constraints or limitations
- `techniques` (List[str]): Specific lateral thinking techniques to apply

**Returns:**
- `dict`: Creative solutions and alternative approaches

#### analyze_decision_tree()

Create and analyze decision trees for complex choices.

**Parameters:**
- `agent_or_team` (Agent): The agent or team to use for analysis
- `decision` (str): The decision to analyze
- `options` (List[str]): Available decision options
- `criteria` (List[str]): Decision criteria to evaluate

**Returns:**
- `dict`: Decision tree analysis with weighted options and recommendations

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits import ThinkingTools

# Initialize toolkit
thinking = ThinkingTools()

# Add to agent
agent = Agent(
    name="Problem Solver",
    model="gpt-4",
    tools=[thinking]
)

# Agent can now use thinking methods
response = agent.run("Use step-by-step thinking to solve this complex problem")
```

## Thinking Methodologies

### Step-by-Step Thinking
- Breaks complex problems into manageable steps
- Provides clear reasoning chain
- Ensures systematic approach to problem solving

### First Principles Thinking
- Challenges existing assumptions
- Breaks down to fundamental truths
- Enables innovative solutions

### Systems Thinking
- Analyzes interconnections and relationships
- Identifies feedback loops and dependencies
- Provides holistic understanding

### Lateral Thinking
- Generates creative and unconventional solutions
- Breaks out of traditional thinking patterns
- Explores alternative approaches

## Related Documentation

- [Thinking Tools Guide](../toolkits/thinking.md)
- [Reasoning Tools API](reasoning.md)
- [StrictToolkit Base](base.md)