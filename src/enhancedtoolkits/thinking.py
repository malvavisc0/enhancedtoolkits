"""
Text-first thinking/journaling utilities for agents:
- Step-by-step thinking chains
- Meta-cognitive reflection
- Working-memory scratchpad
- Quality assessment + synthesis
"""

import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

from agno.utils.log import log_error

from .base import StrictToolkit


# pylint: disable=too-many-instance-attributes
class ThinkingChain:
    """Represents a thinking chain (steps + reflections + scratchpad)."""

    def __init__(self, problem: str, context: Optional[str] = None):
        self.id = self._generate_id()
        self.problem = problem
        self.context = context
        self.steps = []
        self.scratchpad = {}
        self.reflections = []
        self.created_at = datetime.now().isoformat()
        self.confidence_trajectory = []

    # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        self.scratchpad[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat(),
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the thinking chain."""
        return {
            "id": self.id,
            "problem": self.problem,
            "context": self.context,
            "steps_count": len(self.steps),
            "reflections_count": len(self.reflections),
            "avg_confidence": (
                sum(self.confidence_trajectory)
                / len(self.confidence_trajectory)
                if self.confidence_trajectory
                else 0
            ),
            "scratchpad_items": len(self.scratchpad),
            "created_at": self.created_at,
        }

    def _generate_id(self) -> str:
        """Generate unique chain ID."""
        return hashlib.md5(
            f"{datetime.now().isoformat()}_{hash(self)}".encode()
        ).hexdigest()[:8]


class ThinkingTools(StrictToolkit):
    """Text-first thinking/journaling utilities for agents."""

    def __init__(
        self,
        max_chain_length: int = 10,
        confidence_threshold: float = 0.7,
        add_instructions: bool = True,
        **kwargs,
    ):
        self.instructions = """
<thinking_tools>
Thinking/journaling chain (steps/reflections/scratchpad) + synthesis

GOAL
- Build a short step-by-step thinking chain (steps + reflections + scratchpad) and synthesize it.

VALID VALUES
- thinking_type: analysis|synthesis|evaluation|planning|creative|reflection
- synthesis_type: conclusion|summary|insights|next_steps
- scratchpad operation: set|get|list|clear

TOOLS (RETURN TEXT)
- build_step_by_step_reasoning_chain(agent, problem, thinking_type='analysis', context=None, evidence=None, confidence=0.5)
- add_meta_cognitive_reflection(agent, reflection, step_id=None)
- manage_working_memory_scratchpad(agent, key, value=None, operation='set')
- assess_reasoning_chain_quality_and_suggest_improvements(agent)
- synthesize_reasoning_chain_into_output(agent, synthesis_type='conclusion')
- retrieve_current_thinking_chain_state(agent)
- reset_current_thinking_chain(agent)

CONTEXT-SIZE RULES (IMPORTANT)
- Keep steps concise (1-3 sentences). Put bulky text into scratchpad keys.
- When producing user-facing output, call synthesize_reasoning_chain_into_output and summarize.

</thinking_tools>
"""

        super().__init__(
            name="advanced_llm_thinking",
            instructions=self.instructions if add_instructions else "",
            add_instructions=add_instructions,
            **kwargs,
        )

        self.max_chain_length = max_chain_length
        self.confidence_threshold = confidence_threshold

        # Cognitive scaffolding templates (kept intentionally short)
        self.scaffolding_prompts = {
            "analysis": "Identify key components and relations.",
            "synthesis": "Combine pieces into a coherent view.",
            "evaluation": "Check weaknesses, gaps, and counterpoints.",
            "planning": "Outline steps and risks.",
            "creative": "Generate alternatives.",
            "reflection": "Surface assumptions and possible bias.",
        }

        # Register tools
        self.register(self.build_step_by_step_reasoning_chain)
        self.register(self.add_meta_cognitive_reflection)
        self.register(self.manage_working_memory_scratchpad)
        self.register(self.synthesize_reasoning_chain_into_output)
        self.register(
            self.assess_reasoning_chain_quality_and_suggest_improvements
        )
        self.register(self.retrieve_current_thinking_chain_state)
        self.register(self.reset_current_thinking_chain)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def build_step_by_step_reasoning_chain(
        self,
        agent: Any,
        problem: str,
        thinking_type: Optional[str] = "analysis",
        context: Optional[str] = None,
        evidence: Optional[List[str]] = None,
        confidence: float = 0.5,
    ) -> str:
        """Start or continue a thinking chain."""
        if not thinking_type:
            thinking_type = "analysis"
        try:
            session_state = self._get_session_state(agent)

            if "current_chain" not in session_state:
                chain = ThinkingChain(problem, context)
                session_state["current_chain"] = chain
                session_state["all_chains"] = session_state.get(
                    "all_chains", []
                )
                scaffolding = self.scaffolding_prompts.get(
                    thinking_type, "Think step by step:"
                )

                return (
                    f"**Starting {thinking_type.title()} Chain**\n"
                    f"**Problem:** {problem}\n"
                    + (f"**Context:** {context}\n" if context else "")
                    + f"**Cognitive Scaffolding:** {scaffolding}\n"
                    + f"**Chain ID:** {chain.id}\n\n"
                    "**Next Steps:**\n"
                    "1. Add steps with build_step_by_step_reasoning_chain\n"
                    "2. Add reflections with add_meta_cognitive_reflection\n"
                    "3. Use manage_working_memory_scratchpad for working memory\n"
                    "4. Use assess_reasoning_chain_quality_and_suggest_improvements\n"
                    "5. Use synthesize_reasoning_chain_into_output to conclude"
                )

            chain = session_state["current_chain"]
            step = chain.add_step(
                thinking_type,
                problem,
                confidence,
                evidence,
                f"Applied {thinking_type} thinking",
            )

            result = (
                f"**Step {step['id']}: {thinking_type.title()}**\n"
                f"**Reasoning:** {problem}\n"
                f"**Confidence:** {confidence:.1f}/1.0"
            )

            if evidence:
                result += f"\n**Evidence:** {len(evidence)} items"

            if len(chain.steps) < self.max_chain_length:
                next_suggestion = self._suggest_next_steps(thinking_type)
                if next_suggestion:
                    result += f"\n**Suggested Next:** {next_suggestion}"

            if confidence < self.confidence_threshold:
                result += (
                    "\n**Low Confidence** - Consider "
                    "add_meta_cognitive_reflection or "
                    "assess_reasoning_chain_quality_and_suggest_improvements"
                )

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in build_step_by_step_reasoning_chain: {e}")
            return f"Error in reasoning chain: {e}"

    def add_meta_cognitive_reflection(
        self, agent: Any, reflection: str, step_id: Optional[int] = None
    ) -> str:
        """Add meta-cognitive reflection to current thinking chain."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return (
                    "No active thinking chain. Start with "
                    "build_step_by_step_reasoning_chain first."
                )

            chain = session_state["current_chain"]
            chain.add_reflection(reflection, step_id)

            insight = "Valuable meta-cognitive insight"
            if "assumption" in reflection.lower():
                insight = (
                    "Good - questioning assumptions strengthens reasoning"
                )
            elif "bias" in reflection.lower():
                insight = "Excellent - bias awareness improves objectivity"
            elif "alternative" in reflection.lower():
                insight = (
                    "Strong - considering alternatives enhances robustness"
                )

            return (
                f"**Meta-Cognitive Reflection**\n**Reflection:** {reflection}\n"
                + (f"**Reflecting on Step:** {step_id}\n" if step_id else "")
                + f"**Insights:** {insight}\n**Total Reflections:** {len(chain.reflections)}"
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in reflect: {e}")
            return f"Error in reflection: {e}"

    # pylint: disable=too-many-return-statements,too-many-branches
    def manage_working_memory_scratchpad(
        self,
        agent: Any,
        key: str,
        value: Optional[str] = None,
        operation: str = "set",
    ) -> str:
        """Working memory scratchpad for intermediate thoughts and calculations."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return (
                    "No active thinking chain. Start with "
                    "build_step_by_step_reasoning_chain first."
                )

            chain = session_state["current_chain"]

            if operation == "set":
                if value is None:
                    return "Value required for set operation"
                chain.update_scratchpad(key, value)
                return f"**Scratchpad Updated**\n**{key}:** {value}"

            if operation == "get":
                if key in chain.scratchpad:
                    entry = chain.scratchpad[key]
                    return (
                        f"**Scratchpad Entry**\n"
                        f"**{key}:** {entry['value']}\n"
                        f"**Updated:** {entry['updated_at']}"
                    )
                return f"Key '{key}' not found in scratchpad"

            if operation == "list":
                if not chain.scratchpad:
                    return "**Scratchpad Empty**"
                entries = [
                    f"• **{k}:** {v['value']}"
                    for k, v in chain.scratchpad.items()
                ]
                return "**Scratchpad Contents**\n" + "\n".join(entries)

            if operation == "clear":
                if key == "all":
                    chain.scratchpad.clear()
                    return "**Scratchpad Cleared**"
                if key in chain.scratchpad:
                    del chain.scratchpad[key]
                    return f"**Removed:** {key}"
                return f"Key '{key}' not found"

            return (
                f"Unknown operation: {operation}. Use: set, get, list, clear"
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in scratchpad: {e}")
            return f"Error in scratchpad: {e}"

    def synthesize_reasoning_chain_into_output(
        self, agent: Any, synthesis_type: str = "conclusion"
    ) -> str:
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
                synthesis = (
                    f"Analyzed '{chain.problem}' through {len(chain.steps)} steps "
                    f"with {len(chain.reflections)} reflections."
                )
            elif synthesis_type == "insights":
                avg_conf = sum(chain.confidence_trajectory) / len(
                    chain.confidence_trajectory
                )
                synthesis = (
                    f"Key insight: Reasoning progressed with confidence "
                    f"{avg_conf:.1f}. Scratchpad has {len(chain.scratchpad)} items."
                )
            elif synthesis_type == "next_steps":
                synthesis = (
                    "Consider: 1) Gather evidence, 2) Test assumptions, "
                    "3) Explore alternatives"
                )
            else:
                synthesis = (
                    f"Conclusion: Completed analysis of '{chain.problem}' with "
                    "systematic reasoning and reflection."
                )

            # Store completed chain
            session_state["all_chains"].append(chain.get_summary())
            del session_state["current_chain"]

            return (
                f"**{synthesis_type.title()} Synthesis**\n"
                f"**Chain ID:** {chain.id}\n"
                f"**Steps Processed:** {len(chain.steps)}\n"
                f"**Reflections:** {len(chain.reflections)}\n\n"
                f"**{synthesis_type.title()}:**\n{synthesis}"
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in synthesize: {e}")
            return f"Error in synthesis: {e}"

    def assess_reasoning_chain_quality_and_suggest_improvements(
        self, agent: Any
    ) -> str:
        """Evaluate the quality of current thinking chain and suggest improvements."""
        try:
            session_state = self._get_session_state(agent)
            if "current_chain" not in session_state:
                return "No active thinking chain to evaluate."

            chain = session_state["current_chain"]
            assessment = self._assess_chain_quality(chain)

            result = (
                "**Quality Assessment**\n"
                f"**Chain ID:** {chain.id}\n"
                f"**Overall Score:** {assessment['overall_score']:.1f}/5.0\n\n"
                "**Dimensions:**"
            )
            for dimension, score in assessment["dimensions"].items():
                result += f"\n• **{dimension.title()}:** {score:.1f}/5.0"

            if assessment["suggestions"]:
                result += "\n\n**Improvement Suggestions:**"
                for suggestion in assessment["suggestions"]:
                    result += f"\n• {suggestion}"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in quality_check: {e}")
            return f"Error in quality assessment: {e}"

    def _suggest_next_steps(self, current_type: str) -> str:
        """Suggest next reasoning steps."""
        suggestions = {
            "analysis": "Try synthesis or planning",
            "synthesis": "Use evaluation to test the synthesis",
            "evaluation": "Consider reflection or planning",
            "planning": "Summarize into next steps",
            "creative": "Use evaluation or reflection",
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
                5.0,
                sum(len(step.get("evidence", [])) for step in chain.steps) / 2,
            ),
        }

        suggestions = []
        if dimensions["depth"] < 3:
            suggestions.append("Add more reasoning steps for deeper analysis")
        if dimensions["diversity"] < 2:
            suggestions.append(
                "Try different thinking types for broader perspective"
            )
        if dimensions["reflection"] < 2:
            suggestions.append("Add more meta-cognitive reflections")

        return {
            "overall_score": sum(dimensions.values()) / len(dimensions),
            "dimensions": dimensions,
            "suggestions": suggestions,
        }

    def retrieve_current_thinking_chain_state(self, agent: Any) -> str:
        """Get current thinking chain state and history count."""
        session_state = self._get_session_state(agent)
        if "current_chain" not in session_state:
            return "No active thinking chain."

        chain = session_state["current_chain"]
        result = "**Thinking Chain State**\n"
        result += f"**Chain ID:** {chain.id}\n"
        result += f"**Steps:** {len(chain.steps)}\n"
        result += f"**Reflections:** {len(chain.reflections)}\n"
        result += f"**Scratchpad Items:** {len(chain.scratchpad)}\n"
        result += f"**History (completed chains):** {len(session_state.get('all_chains', []))}"
        return result

    def reset_current_thinking_chain(self, agent: Any) -> str:
        """Clear the current thinking chain (does not delete history)."""
        session_state = self._get_session_state(agent)
        if "current_chain" in session_state:
            del session_state["current_chain"]
            return "**Current thinking chain cleared**"
        return "No active thinking chain to clear"

    def _get_session_state(self, agent: Any) -> dict:
        """Get or create session state for agent/team."""
        # pylint: disable=protected-access
        if not hasattr(agent, "_thinking_session_state"):
            agent._thinking_session_state = {}
        return agent._thinking_session_state
