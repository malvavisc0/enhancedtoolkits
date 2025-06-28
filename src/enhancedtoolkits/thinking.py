"""
Advanced LLM Thinking Tool with Tool Planning

A thinking tool designed for LLMs that includes tool orchestration capabilities:
- Structured reasoning chains with intermediate steps
- Self-reflection and meta-cognitive prompts
- General tool planning and orchestration for complex tasks
- Scratchpad for working memory simulation
- Chain-of-thought enhancement with quality gates

Author: malvavisc0
License: MIT
Version: 1.1.0
"""

import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

from agno.utils.log import log_error

from .base import StrictToolkit


class ThinkingChain:
    """Represents a chain of reasoning steps with metadata and tool planning."""

    def __init__(self, problem: str, context: Optional[str] = None):
        self.id = self._generate_id()
        self.problem = problem
        self.context = context
        self.steps = []
        self.scratchpad = {}
        self.reflections = []
        self.tool_plan = []
        self.created_at = datetime.now().isoformat()
        self.confidence_trajectory = []

    def add_step(
        self,
        step_type: str,
        content: str,
        confidence: float = 0.5,
        evidence: Optional[List[str]] = None,
        reasoning: Optional[str] = None,
    ):
        """Add a reasoning step to the chain."""
        step = {
            "id": len(self.steps) + 1,
            "type": step_type,
            "content": content,
            "confidence": confidence,
            "evidence": evidence or [],
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat(),
        }
        self.steps.append(step)
        self.confidence_trajectory.append(confidence)
        return step

    def add_reflection(self, reflection: str, step_id: Optional[int] = None):
        """Add a meta-cognitive reflection."""
        self.reflections.append(
            {
                "content": reflection,
                "step_id": step_id,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def update_scratchpad(self, key: str, value: Any):
        """Update working memory scratchpad."""
        self.scratchpad[key] = {"value": value, "updated_at": datetime.now().isoformat()}

    def add_tool_step(
        self,
        tool_name: str,
        purpose: str,
        inputs: Dict[str, Any],
        dependencies: Optional[List[str]] = None,
    ):
        """Add a tool execution step to the plan."""
        step = {
            "id": len(self.tool_plan) + 1,
            "tool": tool_name,
            "purpose": purpose,
            "inputs": inputs,
            "dependencies": dependencies or [],
            "status": "planned",
            "timestamp": datetime.now().isoformat(),
        }
        self.tool_plan.append(step)
        return step

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the thinking chain."""
        return {
            "id": self.id,
            "problem": self.problem,
            "steps_count": len(self.steps),
            "reflections_count": len(self.reflections),
            "tool_steps": len(self.tool_plan),
            "avg_confidence": (
                sum(self.confidence_trajectory) / len(self.confidence_trajectory)
                if self.confidence_trajectory
                else 0
            ),
            "scratchpad_items": len(self.scratchpad),
            "duration": self.created_at,
        }

    def _generate_id(self) -> str:
        """Generate unique chain ID."""
        return hashlib.md5(
            f"{datetime.now().isoformat()}_{hash(self)}".encode()
        ).hexdigest()[:8]


class EnhancedThinkingTools(StrictToolkit):
    """Advanced LLM Thinking Tool with General Tool Planning and Orchestration"""

    def __init__(
        self,
        max_chain_length: int = 10,
        confidence_threshold: float = 0.7,
        add_instructions: bool = True,
        **kwargs,
    ):

        self.instructions = """
<thinking_instructions>
*** Thinking Tools & General Tool Planning Instructions ***

### Core Thinking Tools
**build_step_by_step_reasoning_chain** - Build step-by-step reasoning chains
- Types: analysis, synthesis, evaluation, planning, creative, reflection, tool_planning
- `thinking_type` is optional and defaults to "analysis".
- Example: `build_step_by_step_reasoning_chain(agent, "What factors affect air quality?")`
- Example (explicit): `build_step_by_step_reasoning_chain(agent, "What factors affect air quality?", "analysis")`

**add_meta_cognitive_reflection** - Add meta-cognitive reflections
- Example: `add_meta_cognitive_reflection(agent, "Am I missing behavioral factors?")`

**manage_working_memory_scratchpad** - Working memory for data, assumptions, insights
- Operations: set, get, list, clear

**synthesize_reasoning_chain_into_output** - Combine reasoning into conclusions or insights
- Types: conclusion, summary, insights, next_steps
- Example: `synthesize_reasoning_chain_into_output(agent, "conclusion")`

**assess_reasoning_chain_quality_and_suggest_improvements** - Evaluate reasoning quality and suggest improvements

### General Tool Planning & Orchestration
**create_general_tool_execution_plan** - Create flexible tool sequences for any task
- Analyzes available tools and creates general workflow patterns
- Provides context hints without making rigid assumptions
- Example: `create_general_tool_execution_plan(agent, "Create web dashboard", ["read_file", "write_file", "browser_action"], "responsive design")`

**execute_and_monitor_tool_plan** - Execute planned tool sequences with monitoring
- Actions: execute, status, complete_step
- Example: `execute_and_monitor_tool_plan(agent, "execute")`

### General Planning Features
- **Flexible Tool Selection**: Chooses tools based on availability, not assumptions
- **Generic Dependencies**: Creates logical workflow patterns (info → create → test)
- **Context Hints**: Provides guidance without forcing specific implementations
- **LLM Customization**: Uses "to_be_specified_by_llm" for maximum flexibility

### Workflow Patterns
**General Analysis:** build_step_by_step_reasoning_chain(analysis) → manage_working_memory_scratchpad(context) → create_general_tool_execution_plan → execute_and_monitor_tool_plan

**Flexible Development:** create_general_tool_execution_plan(task, available_tools, context) → execute_and_monitor_tool_plan → add_meta_cognitive_reflection → synthesize_reasoning_chain_into_output

### Tool Planning Example: General Approach
```
1. build_step_by_step_reasoning_chain(agent, "Create interactive dashboard", "planning")
2. manage_working_memory_scratchpad(agent, "requirements", "Charts, responsive design, real-time data")
3. create_general_tool_execution_plan(agent, "Create web dashboard", tools, "responsive design with charts")
4. execute_and_monitor_tool_plan(agent, "execute")  # LLM customizes each step
5. add_meta_cognitive_reflection(agent, "Does the plan address all requirements?")
6. synthesize_reasoning_chain_into_output(agent, "project_completion")
```
</thinking_instructions>
"""

        super().__init__(
            name="advanced_llm_thinking",
            instructions=self.instructions if add_instructions else "",
            add_instructions=add_instructions,
            **kwargs,
        )

        self.max_chain_length = max_chain_length
        self.confidence_threshold = confidence_threshold

        # Cognitive scaffolding templates
        self.scaffolding_prompts = {
            "analysis": "Break this down: What are the key components? How do they relate?",
            "synthesis": "Combine insights: What patterns emerge? How do pieces fit together?",
            "evaluation": "Assess critically: What are strengths/weaknesses? What's missing?",
            "planning": "Think ahead: What steps are needed? What could go wrong?",
            "creative": "Think differently: What alternatives exist? What if we changed X?",
            "reflection": "Think about thinking: How did I approach this? What assumptions did I make?",
            "tool_planning": "Tool sequence: What tools are needed? In what order? What dependencies?",
        }

        # Register tools
        self.register(self.build_step_by_step_reasoning_chain)
        self.register(self.add_meta_cognitive_reflection)
        self.register(self.manage_working_memory_scratchpad)
        self.register(self.synthesize_reasoning_chain_into_output)
        self.register(self.assess_reasoning_chain_quality_and_suggest_improvements)
        self.register(self.create_general_tool_execution_plan)
        self.register(self.execute_and_monitor_tool_plan)

    def build_step_by_step_reasoning_chain(
        self,
        agent: Any,
        problem: str,
        thinking_type: Optional[str] = "analysis",
        context: Optional[str] = None,
        evidence: Optional[List[str]] = None,
        confidence: float = 0.5,
    ) -> str:
        """
        Start or continue a structured reasoning chain.

        Args:
            agent: The agent or team context.
            problem: The problem or question to reason about.
            thinking_type: (optional) The type of reasoning to use (e.g., "analysis", "planning", etc.). Defaults to "analysis".
            context: (optional) Additional context for the reasoning step.
            evidence: (optional) List of evidence strings.
            confidence: (optional) Confidence score for the step.

        Returns:
            str: Result of the reasoning step.
        """
        if not thinking_type:
            thinking_type = "analysis"
        try:
            session_state = self._get_session_state(agent)

            if "current_chain" not in session_state:
                chain = ThinkingChain(problem, context)
                session_state["current_chain"] = chain
                session_state["all_chains"] = session_state.get("all_chains", [])
                scaffolding = self.scaffolding_prompts.get(
                    thinking_type, "Think step by step:"
                )

                return (
                    f"**Starting {thinking_type.title()} Chain**\n**Problem:** {problem}\n"
                    + (f"**Context:** {context}\n" if context else "")
                    + f"**Cognitive Scaffolding:** {scaffolding}\n**Chain ID:** {chain.id}\n\n"
                    + "**Next Steps:**\n1. Use chain_think to add reasoning steps\n2. Use reflect for meta-cognitive insights\n3. Use scratchpad for working memory"
                )
            else:
                chain = session_state["current_chain"]
                step = chain.add_step(
                    thinking_type,
                    problem,
                    confidence,
                    evidence,
                    f"Applied {thinking_type} thinking",
                )

                result = f"**Step {step['id']}: {thinking_type.title()}**\n**Reasoning:** {problem}\n**Confidence:** {confidence:.1f}/1.0"
                if evidence:
                    result += f"\n**Evidence:** {len(evidence)} items"
                if len(chain.steps) < self.max_chain_length:
                    next_suggestion = self._suggest_next_steps(thinking_type)
                    if next_suggestion:
                        result += f"\n**Suggested Next:** {next_suggestion}"
                if confidence < self.confidence_threshold:
                    result += (
                        f"\n**Low Confidence** - Consider using reflect or quality_check"
                    )
                return result

        except Exception as e:
            log_error(f"Error in chain_think: {e}")
            return f"Error in reasoning chain: {e}"

    def add_meta_cognitive_reflection(self, agent: Any, reflection: str, step_id: Optional[int] = None) -> str:
        """Add meta-cognitive reflection to current thinking chain."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain. Start with build_step_by_step_reasoning_chain first."
            if "current_chain" not in session_state:
                return "No active thinking chain. Start with build_step_by_step_reasoning_chain first."
            if "current_chain" not in session_state:
                return "No active thinking chain. Start with build_step_by_step_reasoning_chain first."

            chain = session_state["current_chain"]
            chain.add_reflection(reflection, step_id)

            insight = "Valuable meta-cognitive insight"
            if "assumption" in reflection.lower():
                insight = "Good - questioning assumptions strengthens reasoning"
            elif "bias" in reflection.lower():
                insight = "Excellent - bias awareness improves objectivity"
            elif "alternative" in reflection.lower():
                insight = "Strong - considering alternatives enhances robustness"

            return (
                f"**Meta-Cognitive Reflection**\n**Reflection:** {reflection}\n"
                + (f"**Reflecting on Step:** {step_id}\n" if step_id else "")
                + f"**Insights:** {insight}\n**Total Reflections:** {len(chain.reflections)}"
            )

        except Exception as e:
            log_error(f"Error in reflect: {e}")
            return f"Error in reflection: {e}"

    def manage_working_memory_scratchpad(
        self, agent: Any, key: str, value: Optional[str] = None, operation: str = "set"
    ) -> str:
        """Working memory scratchpad for intermediate thoughts and calculations."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain. Start with chain_think first."

            chain = session_state["current_chain"]

            if operation == "set":
                if value is None:
                    return "Value required for set operation"
                chain.update_scratchpad(key, value)
                return f"**Scratchpad Updated**\n**{key}:** {value}"
            elif operation == "get":
                if key in chain.scratchpad:
                    entry = chain.scratchpad[key]
                    return f"**Scratchpad Entry**\n**{key}:** {entry['value']}\n**Updated:** {entry['updated_at']}"
                else:
                    return f"Key '{key}' not found in scratchpad"
            elif operation == "list":
                if not chain.scratchpad:
                    return "**Scratchpad Empty**"
                entries = [
                    f"• **{k}:** {v['value']}" for k, v in chain.scratchpad.items()
                ]
                return f"**Scratchpad Contents**\n" + "\n".join(entries)
            elif operation == "clear":
                if key == "all":
                    chain.scratchpad.clear()
                    return "**Scratchpad Cleared**"
                elif key in chain.scratchpad:
                    del chain.scratchpad[key]
                    return f"**Removed:** {key}"
                else:
                    return f"Key '{key}' not found"
            else:
                return f"Unknown operation: {operation}. Use: set, get, list, clear"

        except Exception as e:
            log_error(f"Error in scratchpad: {e}")
            return f"Error in scratchpad: {e}"

    def synthesize_reasoning_chain_into_output(self, agent: Any, synthesis_type: str = "conclusion") -> str:
        """Synthesize current thinking chain into insights or conclusions."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain to synthesize."

            chain = session_state["current_chain"]
            if not chain.steps:
                return "No reasoning steps to synthesize."

            # Generate synthesis based on type
            if synthesis_type == "summary":
                synthesis = f"Analyzed '{chain.problem}' through {len(chain.steps)} steps with {len(chain.reflections)} reflections."
            elif synthesis_type == "insights":
                avg_conf = sum(chain.confidence_trajectory) / len(
                    chain.confidence_trajectory
                )
                synthesis = f"Key insight: Reasoning progressed with confidence {avg_conf:.1f}. Scratchpad has {len(chain.scratchpad)} items."
            elif synthesis_type == "next_steps":
                synthesis = "Consider: 1) Gathering evidence, 2) Testing assumptions, 3) Exploring alternatives"
            else:
                synthesis = f"Conclusion: Completed analysis of '{chain.problem}' with systematic reasoning and reflection."

            # Store completed chain
            session_state["all_chains"].append(chain.get_summary())
            del session_state["current_chain"]

            return (
                f"**{synthesis_type.title()} Synthesis**\n**Chain ID:** {chain.id}\n"
                + f"**Steps Processed:** {len(chain.steps)}\n**Reflections:** {len(chain.reflections)}\n\n"
                + f"**{synthesis_type.title()}:**\n{synthesis}"
            )

        except Exception as e:
            log_error(f"Error in synthesize: {e}")
            return f"Error in synthesis: {e}"

    def assess_reasoning_chain_quality_and_suggest_improvements(self, agent: Any) -> str:
        """Evaluate the quality of current thinking chain and suggest improvements."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain to evaluate."

            chain = session_state["current_chain"]
            assessment = self._assess_chain_quality(chain)

            result = f"**Quality Assessment**\n**Chain ID:** {chain.id}\n**Overall Score:** {assessment['overall_score']:.1f}/5.0\n\n**Dimensions:**"
            for dimension, score in assessment["dimensions"].items():
                result += f"\n• **{dimension.title()}:** {score:.1f}/5.0"

            if assessment["suggestions"]:
                result += "\n\n**Improvement Suggestions:**"
                for suggestion in assessment["suggestions"]:
                    result += f"\n• {suggestion}"

            return result

        except Exception as e:
            log_error(f"Error in quality_check: {e}")
            return f"Error in quality assessment: {e}"

    def create_general_tool_execution_plan(
        self,
        agent: Any,
        task: str,
        available_tools: List[str],
        context: Optional[str] = None,
    ) -> str:
        """Plan tool sequence for complex tasks using general approach."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "Start with build_step_by_step_reasoning_chain first to establish reasoning context."

            chain = session_state["current_chain"]

            # Add tool planning step to reasoning chain
            chain.add_step(
                "tool_planning",
                f"Planning tool sequence for: {task}",
                0.8,
                available_tools,
                "Creating general tool workflow with context guidance",
            )

            # Generate general tool plan
            tool_sequence = self._generate_tool_plan(task, available_tools, context)

            # Store tool plan
            for step in tool_sequence:
                chain.add_tool_step(
                    tool_name=step["tool"],
                    purpose=step["purpose"],
                    inputs=step["inputs"],
                    dependencies=step["dependencies"],
                )

            result = f"🛠️ **General Tool Planning Complete**\n**Task:** {task}\n**Context:** {context or 'None'}\n**Available Tools:** {len(available_tools)}\n**Planned Steps:** {len(tool_sequence)}\n\n**Tool Sequence:**"

            for i, step in enumerate(tool_sequence, 1):
                deps = (
                    f" (depends on: {', '.join(step['dependencies'])})"
                    if step["dependencies"]
                    else ""
                )
                result += f"\n{i}. **{step['tool']}** - {step['purpose']}{deps}"

            result += "\n\n**Next:** Use execute_and_monitor_tool_plan(agent, 'execute') to run the plan"
            return result

        except Exception as e:
            log_error(f"Error in plan_tools: {e}")
            return f"Error in tool planning: {e}"

    def execute_and_monitor_tool_plan(self, agent: Any, action: str = "execute") -> str:
        """Execute and monitor tool plans."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain with tool plan."

            chain = session_state["current_chain"]
            if not chain.tool_plan:
                return "No tool plan found. Use create_general_tool_execution_plan first."

            if action == "execute":
                ready_steps = [
                    s
                    for s in chain.tool_plan
                    if s["status"] == "planned"
                    and self._dependencies_met(s, chain.tool_plan)
                ]

                if not ready_steps:
                    completed = len(
                        [s for s in chain.tool_plan if s["status"] == "completed"]
                    )
                    return f"**Tool Plan Complete** - {completed}/{len(chain.tool_plan)} steps finished"

                next_step = ready_steps[0]
                next_step["status"] = "ready"

                return f"**Ready to Execute**\n**Tool:** {next_step['tool']}\n**Purpose:** {next_step['purpose']}\n**Inputs:** {next_step['inputs']}\n\n**Action Required:** Execute this tool, then call orchestrate again"

            elif action == "status":
                status_counts = {}
                for step in chain.tool_plan:
                    status_counts[step["status"]] = (
                        status_counts.get(step["status"], 0) + 1
                    )
                return f"**Plan Status:** {dict(status_counts)}"

            elif action == "complete_step":
                ready_steps = [s for s in chain.tool_plan if s["status"] == "ready"]
                if ready_steps:
                    ready_steps[0]["status"] = "completed"
                    return (
                        "**Step Completed** - Call orchestrate('execute') for next step"
                    )
                return "No ready steps to complete"

            else:
                return f"Unknown action: {action}. Use: execute, status, complete_step"

        except Exception as e:
            log_error(f"Error in orchestrate: {e}")
            return f"Error in orchestration: {e}"

    def _generate_tool_plan(
        self, task: str, available_tools: List[str], context: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Generate general tool execution plan based on available tools and context hints."""
        plan = []

        # Step 1: Information gathering (if applicable tools available)
        info_tools = [
            tool
            for tool in available_tools
            if tool
            in ["read_file", "list_files", "search_files", "list_code_definition_names"]
        ]
        if info_tools:
            plan.append(
                {
                    "tool": info_tools[0],
                    "purpose": f"Gather information for: {task}",
                    "inputs": self._get_generic_inputs(info_tools[0], context),
                    "dependencies": [],
                }
            )

        # Step 2: Processing/Creation (if applicable tools available)
        creation_tools = [
            tool
            for tool in available_tools
            if tool
            in ["write_to_file", "apply_diff", "insert_content", "search_and_replace"]
        ]
        if creation_tools:
            deps = [plan[0]["tool"]] if plan else []
            plan.append(
                {
                    "tool": creation_tools[0],
                    "purpose": f"Create/modify content for: {task}",
                    "inputs": self._get_generic_inputs(creation_tools[0], context),
                    "dependencies": deps,
                }
            )

        # Step 3: Execution/Testing (if applicable tools available)
        execution_tools = [
            tool
            for tool in available_tools
            if tool in ["execute_command", "browser_action", "use_mcp_tool"]
        ]
        if execution_tools:
            deps = [step["tool"] for step in plan if step["tool"] in creation_tools]
            plan.append(
                {
                    "tool": execution_tools[0],
                    "purpose": f"Execute/test for: {task}",
                    "inputs": self._get_generic_inputs(execution_tools[0], context),
                    "dependencies": deps,
                }
            )

        # If no specific tools match common patterns, create a flexible manual step
        if not plan:
            plan.append(
                {
                    "tool": "manual_planning_required",
                    "purpose": f"Custom tool sequence needed for: {task}",
                    "inputs": {
                        "task": task,
                        "context": context or "No context provided",
                        "available_tools": available_tools,
                        "suggestion": "LLM should manually plan tool sequence based on specific requirements",
                    },
                    "dependencies": [],
                }
            )

        return plan

    def _get_generic_inputs(
        self, tool_name: str, context: Optional[str]
    ) -> Dict[str, Any]:
        """Generate generic input templates for tools based on context hints."""
        context_hint = (
            f"Consider context: {context}"
            if context
            else "Specify parameters based on task requirements"
        )

        # Simplified input templates
        templates = {
            "read_file": {"path": "to_be_specified_by_llm", "context_hint": context_hint},
            "list_files": {"path": ".", "recursive": True, "context_hint": context_hint},
            "search_files": {
                "path": ".",
                "regex": "to_be_specified_by_llm",
                "context_hint": context_hint,
            },
            "list_code_definition_names": {"path": ".", "context_hint": context_hint},
            "write_to_file": {
                "path": "to_be_specified_by_llm",
                "content": "to_be_generated_by_llm",
                "context_hint": context_hint,
            },
            "apply_diff": {
                "path": "to_be_specified_by_llm",
                "diff": "to_be_generated_by_llm",
                "context_hint": context_hint,
            },
            "insert_content": {
                "path": "to_be_specified_by_llm",
                "line": 0,
                "content": "to_be_generated_by_llm",
                "context_hint": context_hint,
            },
            "search_and_replace": {
                "path": "to_be_specified_by_llm",
                "search": "to_be_specified_by_llm",
                "replace": "to_be_specified_by_llm",
                "context_hint": context_hint,
            },
            "execute_command": {
                "command": "to_be_specified_by_llm",
                "context_hint": context_hint,
            },
            "browser_action": {
                "action": "launch",
                "url": "to_be_specified_by_llm",
                "context_hint": context_hint,
            },
            "use_mcp_tool": {
                "server_name": "to_be_specified_by_llm",
                "tool_name": "to_be_specified_by_llm",
                "arguments": {},
                "context_hint": context_hint,
            },
        }

        return templates.get(
            tool_name,
            {"parameters": "to_be_specified_by_llm", "context_hint": context_hint},
        )

    def _dependencies_met(
        self, step: Dict[str, Any], all_steps: List[Dict[str, Any]]
    ) -> bool:
        """Check if step dependencies are met."""
        if not step["dependencies"]:
            return True
        completed_tools = {s["tool"] for s in all_steps if s["status"] == "completed"}
        return all(dep in completed_tools for dep in step["dependencies"])

    def _suggest_next_steps(self, current_type: str) -> str:
        """Suggest next reasoning steps."""
        suggestions = {
            "analysis": "Try synthesis or plan_tools for implementation",
            "synthesis": "Use evaluation to assess insights",
            "evaluation": "Consider planning or tool planning",
            "planning": "Use plan_tools for tool orchestration",
            "tool_planning": "Use orchestrate to execute plan",
            "creative": "Use reflection to assess new ideas",
            "reflection": "Return to analysis with new perspective",
        }
        return suggestions.get(current_type, "Continue with deeper analysis")

    def _assess_chain_quality(self, chain: ThinkingChain) -> Dict[str, Any]:
        """Assess chain quality."""
        step_diversity = len(set(step["type"] for step in chain.steps))
        avg_confidence = (
            sum(chain.confidence_trajectory) / len(chain.confidence_trajectory)
            if chain.confidence_trajectory
            else 0
        )
        reflection_ratio = len(chain.reflections) / max(1, len(chain.steps))

        dimensions = {
            "depth": min(5.0, len(chain.steps) / 2),
            "diversity": min(5.0, step_diversity),
            "confidence": avg_confidence * 5,
            "reflection": min(5.0, reflection_ratio * 10),
            "evidence": min(
                5.0, sum(len(step.get("evidence", [])) for step in chain.steps) / 2
            ),
        }

        suggestions = []
        if dimensions["depth"] < 3:
            suggestions.append("Add more reasoning steps for deeper analysis")
        if dimensions["diversity"] < 2:
            suggestions.append("Try different thinking types for broader perspective")
        if dimensions["reflection"] < 2:
            suggestions.append("Add more meta-cognitive reflections")

        return {
            "overall_score": sum(dimensions.values()) / len(dimensions),
            "dimensions": dimensions,
            "suggestions": suggestions,
        }

    def _get_session_state(self, agent: Any) -> dict:
        """Get session state."""
        if isinstance(agent, dict):
            return agent.setdefault("session_state", {})
        elif hasattr(agent, "session_state"):
            if agent.session_state is None:
                agent.session_state = {}
            return agent.session_state
        else:
            try:
                if not hasattr(agent, "__dict__"):
                    agent.__dict__ = {}
                agent.__dict__["session_state"] = agent.__dict__.get("session_state", {})
                return agent.__dict__["session_state"]
            except (AttributeError, TypeError):
                return {}
