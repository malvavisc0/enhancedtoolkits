# Reasoning Tools

The Reasoning Tools provide multi-modal reasoning capabilities with cognitive bias detection and session management for AI agents.

## Overview

The `ReasoningTools` class offers sophisticated reasoning capabilities that help AI agents think through complex problems using various reasoning methodologies while detecting and mitigating cognitive biases.

## Key Features

- **6 Reasoning Types**: Deductive, Inductive, Abductive, Causal, Probabilistic, Analogical
- **Bias Detection**: Automatic identification of cognitive biases
- **Session Tracking**: Reasoning step history and workflow management
- **Quality Assessment**: Confidence levels and evidence evaluation
- **Multi-modal Integration**: Combine multiple reasoning approaches

## Installation

```bash
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

## Basic Usage

```python
from enhancedtoolkits import ReasoningTools

# Initialize reasoning tools
reasoning = ReasoningTools(
    reasoning_depth=5,
    enable_bias_detection=True,
    instructions="Custom reasoning instructions..."
)
```

## Available Methods

### `reason()`

Apply specific reasoning type to a problem.

```python
result = reasoning.reason(
    agent_or_team=agent,
    problem="Should we invest in renewable energy?",
    reasoning_type="analytical",
    evidence=[
        "Government incentives increasing",
        "Technology costs decreasing",
        "Market demand growing"
    ],
    context="Investment decision for Q4 2024"
)
```

**Parameters:**
- `agent_or_team`: Your agent instance for session tracking
- `problem` (str): The problem to reason about
- `reasoning_type` (str): Type of reasoning to apply
- `evidence` (List[str]): Supporting evidence
- `context` (str, optional): Additional context

### `multi_modal_reason()`

Combine multiple reasoning approaches for complex problems.

```python
result = reasoning.multi_modal_reason(
    agent_or_team=agent,
    problem="Evaluate market entry strategy",
    reasoning_types=["analytical", "probabilistic", "causal"],
    evidence=[
        "Market size: $50B",
        "Competition: 5 major players",
        "Our competitive advantage: AI technology"
    ]
)
```

### `analyze_reasoning()`

Evaluate reasoning results and determine next actions.

```python
analysis = reasoning.analyze_reasoning(
    agent_or_team=agent,
    reasoning_content="Previous reasoning output...",
    focus_areas=["evidence_strength", "logical_consistency"]
)
```

### `detect_biases()`

Identify cognitive biases in reasoning content.

```python
bias_analysis = reasoning.detect_biases(
    agent_or_team=agent,
    reasoning_content="Our analysis shows..."
)
```

### `get_reasoning_history()`

Retrieve session reasoning history.

```python
history = reasoning.get_reasoning_history(agent_or_team=agent)
```

## Reasoning Types

### Analytical Reasoning
Systematic breakdown of complex problems into components.

```python
result = reasoning.reason(
    agent_or_team=agent,
    problem="Optimize supply chain efficiency",
    reasoning_type="analytical",
    evidence=["Current bottlenecks", "Cost analysis", "Performance metrics"]
)
```

### Probabilistic Reasoning
Reasoning under uncertainty with probability assessments.

```python
result = reasoning.reason(
    agent_or_team=agent,
    problem="Predict market trends",
    reasoning_type="probabilistic",
    evidence=["Historical data", "Market indicators", "Expert opinions"]
)
```

### Causal Reasoning
Understanding cause-and-effect relationships.

```python
result = reasoning.reason(
    agent_or_team=agent,
    problem="Why did sales decline?",
    reasoning_type="causal",
    evidence=["Sales data", "Market conditions", "Product changes"]
)
```

## Bias Detection

The system automatically detects common cognitive biases:

- **Confirmation Bias**: Seeking information that confirms existing beliefs
- **Anchoring Bias**: Over-relying on first information received
- **Availability Heuristic**: Overestimating likelihood of memorable events
- **Overconfidence Bias**: Overestimating one's own abilities
- **Sunk Cost Fallacy**: Continuing based on previously invested resources

## Configuration Options

```python
reasoning = ReasoningTools(
    reasoning_depth=5,              # Maximum reasoning steps
    enable_bias_detection=True,     # Enable cognitive bias detection
    enable_quality_assessment=True, # Enable quality metrics
    instructions="Custom instructions for reasoning process"
)
```

## Advanced Examples

### Investment Decision Analysis

```python
def analyze_investment_opportunity():
    reasoning = ReasoningTools(enable_bias_detection=True)
    
    # Multi-modal reasoning for investment decision
    result = reasoning.multi_modal_reason(
        agent_or_team=agent,
        problem="Should we invest $1M in AI startup XYZ?",
        reasoning_types=["analytical", "probabilistic", "causal"],
        evidence=[
            "Startup has 50% YoY growth",
            "Market size: $10B by 2025",
            "Team has 2 successful exits",
            "Current valuation: $50M",
            "Competitive landscape: 20+ players"
        ]
    )
    
    # Analyze for biases
    bias_check = reasoning.detect_biases(
        agent_or_team=agent,
        reasoning_content=result
    )
    
    return result, bias_check
```

### Strategic Planning

```python
def strategic_planning_session():
    reasoning = ReasoningTools(reasoning_depth=7)
    
    # Iterative reasoning for complex strategy
    result = reasoning.iterative_reason(
        agent_or_team=agent,
        problem="Develop 5-year growth strategy",
        max_iterations=5,
        evidence=[
            "Current market position",
            "Resource constraints",
            "Competitive threats",
            "Technology trends"
        ]
    )
    
    # Get reasoning history
    history = reasoning.get_reasoning_history(agent_or_team=agent)
    
    return result, history
```

## Error Handling

```python
try:
    result = reasoning.reason(
        agent_or_team=agent,
        problem="Complex problem",
        reasoning_type="analytical",
        evidence=["Evidence 1", "Evidence 2"]
    )
except ReasoningError as e:
    print(f"Reasoning error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Best Practices

1. **Provide Quality Evidence**: Include diverse, credible evidence sources
2. **Use Appropriate Reasoning Types**: Match reasoning type to problem nature
3. **Enable Bias Detection**: Always check for cognitive biases
4. **Review Reasoning History**: Learn from previous reasoning sessions
5. **Combine Multiple Types**: Use multi-modal reasoning for complex decisions

## Performance Tips

- Enable caching for repeated reasoning patterns
- Use session management for related reasoning tasks
- Monitor reasoning depth to balance quality and performance
- Regular bias detection helps improve reasoning quality

## Related Tools

- [Thinking Tools](thinking.md) - Structured cognitive frameworks
- [Calculator Tools](../calculators/index.md) - Mathematical reasoning support
- [Finance Tools](finance.md) - Financial data for reasoning

## API Reference

For complete API documentation, see the [API Reference](../api/reasoning.md).
