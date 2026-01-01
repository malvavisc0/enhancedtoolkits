"""
Enhanced Universal Reasoning Tools v5.0

A simplified, LLM-optimized reasoning toolkit that combines:
- Multi-modal reasoning with string-based types
- Meta-cognitive capabilities (reflection, working memory)
- Bias detection with iterative correction
- Flexible cognitive modes and quality assessment

Author: malvavisc0
License: MIT
Version: 5.0.0
"""

import hashlib
from datetime import datetime
from typing import Any, List, Optional

from agno.utils.log import log_debug, log_error

from .base import StrictToolkit

# String constants replacing Enums
REASONING_TYPES = [
    "deductive",
    "inductive",
    "abductive",
    "causal",
    "probabilistic",
    "analogical",
]
COGNITIVE_MODES = [
    "analysis",
    "synthesis",
    "evaluation",
    "planning",
    "creative",
    "reflection",
]


class EnhancedReasoningTools(StrictToolkit):
    """Enhanced Universal Reasoning Tools v5.0.

    Text-first reasoning utilities with lightweight session state.
    """

    def __init__(
        self,
        reasoning_depth: int = 5,
        enable_bias_detection: bool = True,
        add_instructions: bool = True,
        **kwargs,
    ):
        self.instructions = """
<reasoning_tools>
Record, review, and improve an agent's reasoning process.

Guidelines:
- Keep steps short and concrete; include evidence when available.
- Prefer alternating analysis → synthesis → evaluation, then synthesize.

Valid values:
- cognitive_mode: analysis|synthesis|evaluation|planning|creative|reflection
- reasoning_type: deductive|inductive|abductive|causal|probabilistic|analogical

Primary tools:
- add_structured_reasoning_step(agent, problem, cognitive_mode='analysis',
  reasoning_type='deductive', evidence=None, confidence=0.5)
- add_meta_cognitive_reflection(agent, reflection, step_id=None)
- manage_working_memory_scratchpad(agent, key, value=None,
  operation='set|get|list|clear')
- assess_reasoning_quality_and_suggest_improvements(agent)
- synthesize_reasoning_chain_into_conclusion_or_insight(agent,
  synthesis_type='conclusion|summary|insights')

Session:
- retrieve_current_reasoning_session_state(agent)
- reset_reasoning_session_state(agent)
</reasoning_tools>
"""

        super().__init__(
            name="enhanced_reasoning_tools_v5",
            instructions=self.instructions if add_instructions else "",
            add_instructions=add_instructions,
            **kwargs,
        )

        self.reasoning_depth = max(1, min(10, reasoning_depth))
        self.enable_bias_detection = enable_bias_detection

        # Bias detection patterns
        self.bias_patterns = {
            "confirmation_bias": [
                "confirms",
                "supports",
                "validates",
                "proves",
                "obviously",
                "clearly",
            ],
            "anchoring_bias": [
                "first",
                "initial",
                "starting",
                "baseline",
                "reference",
            ],
            "availability_heuristic": [
                "recent",
                "memorable",
                "vivid",
                "comes to mind",
                "recall",
            ],
            "overconfidence_bias": [
                "definitely",
                "certainly",
                "absolutely",
                "guaranteed",
                "impossible",
            ],
        }

        # Cognitive scaffolding prompts (kept intentionally short)
        self.cognitive_prompts = {
            "analysis": "Identify key components and relations.",
            "synthesis": "Combine pieces into a coherent view.",
            "evaluation": "Check weaknesses, gaps, and counterpoints.",
            "planning": "Outline steps, risks, and contingencies.",
            "creative": "Generate alternatives and reframes.",
            "reflection": "Surface assumptions and possible bias.",
        }

        # Register tools (keep the default API small; opt-in extras via flags)
        self.register(self.add_structured_reasoning_step)
        self.register(self.add_meta_cognitive_reflection)
        self.register(self.manage_working_memory_scratchpad)
        self.register(self.assess_reasoning_quality_and_suggest_improvements)
        self.register(self.retrieve_current_reasoning_session_state)
        self.register(
            self.synthesize_reasoning_chain_into_conclusion_or_insight
        )
        self.register(self.reset_reasoning_session_state)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def add_structured_reasoning_step(
        self,
        agent_or_team: Any,
        problem: str,
        cognitive_mode: str = "analysis",
        reasoning_type: str = "deductive",
        evidence: Optional[List[str]] = None,
        confidence: float = 0.5,
    ) -> str:
        """Add a structured reasoning step with cognitive mode and type."""
        try:
            # Validate inputs
            if cognitive_mode not in COGNITIVE_MODES:
                cognitive_mode = "analysis"
            if reasoning_type not in REASONING_TYPES:
                reasoning_type = "deductive"

            log_debug(
                f"Reasoning step ({cognitive_mode}/{reasoning_type}): {problem[:50]}..."
            )

            session_state = self._get_session_state(agent_or_team)

            # Initialize session if needed
            if "reasoning_chain" not in session_state:
                session_state["reasoning_chain"] = {
                    "id": self._generate_id(),
                    "steps": [],
                    "reflections": [],
                    "scratchpad": {},
                    "created_at": datetime.now().isoformat(),
                    "confidence_trajectory": [],
                }

            chain = session_state["reasoning_chain"]

            # Detect biases if enabled
            biases_detected = []
            if self.enable_bias_detection:
                biases_detected = self._detect_biases_in_content(
                    problem, evidence or []
                )

            # Create reasoning step
            step = {
                "id": len(chain["steps"]) + 1,
                "cognitive_mode": cognitive_mode,
                "reasoning_type": reasoning_type,
                "content": problem,
                "confidence": confidence,
                "evidence": evidence or [],
                "biases_detected": biases_detected,
                "timestamp": datetime.now().isoformat(),
            }

            chain["steps"].append(step)
            chain["confidence_trajectory"].append(confidence)

            # Keep output compact: only show scaffolding when confidence is low.
            scaffolding = self.cognitive_prompts.get(
                cognitive_mode, "Think step by step:"
            )

            result = f"**Step {step['id']}: {cognitive_mode.title()} ({reasoning_type})**\n"
            result += f"**Problem:** {problem}\n"
            result += f"**Confidence:** {confidence:.1f}/1.0\n"

            if confidence < 0.7:
                result += f"**Scaffolding:** {scaffolding}\n"

            if evidence:
                result += f"**Evidence:** {len(evidence)} items\n"

            if biases_detected:
                bias_names = [
                    b.replace("_", " ").title() for b in biases_detected
                ]
                result += f"**Biases Detected:** {', '.join(bias_names)}\n"

            if confidence < 0.7:
                result += "**Low Confidence** - Consider reflection or quality check\n"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in add_structured_reasoning_step: {e}")
            return f"Error in reasoning step: {e}"

    def add_meta_cognitive_reflection(
        self,
        agent_or_team: Any,
        reflection: str,
        step_id: Optional[int] = None,
    ) -> str:
        """Add meta-cognitive reflection to current reasoning chain."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" not in session_state:
                return "No active reasoning chain. Start with add_structured_reasoning_step first."

            chain = session_state["reasoning_chain"]

            reflection_entry = {
                "content": reflection,
                "step_id": step_id,
                "timestamp": datetime.now().isoformat(),
            }

            chain["reflections"].append(reflection_entry)

            # Provide insight based on reflection content
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

            result = "**Meta-Cognitive Reflection**\n"
            result += f"**Reflection:** {reflection}\n"
            if step_id:
                result += f"**Reflecting on Step:** {step_id}\n"
            result += f"**Insight:** {insight}\n"
            result += f"**Total Reflections:** {len(chain['reflections'])}"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in reflect: {e}")
            return f"Error in reflection: {e}"

    # pylint: disable=too-many-return-statements,too-many-branches
    def manage_working_memory_scratchpad(
        self,
        agent_or_team: Any,
        key: str,
        value: Optional[str] = None,
        operation: str = "set",
    ) -> str:
        """Working memory scratchpad for intermediate thoughts and data."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" not in session_state:
                return "No active reasoning chain. Start with add_structured_reasoning_step first."

            chain = session_state["reasoning_chain"]

            if operation == "set":
                if value is None:
                    return "Value required for set operation"
                chain["scratchpad"][key] = {
                    "value": value,
                    "updated_at": datetime.now().isoformat(),
                }
                return f"**Scratchpad Updated**\n**{key}:** {value}"

            if operation == "get":
                if key in chain["scratchpad"]:
                    entry = chain["scratchpad"][key]
                    return (
                        f"**Scratchpad Entry**\n"
                        f"**{key}:** {entry['value']}\n"
                        f"**Updated:** {entry['updated_at']}"
                    )
                return f"Key '{key}' not found in scratchpad"

            if operation == "list":
                if not chain["scratchpad"]:
                    return "**Scratchpad Empty**"
                entries = [
                    f"• **{k}:** {v['value']}"
                    for k, v in chain["scratchpad"].items()
                ]
                return "**Scratchpad Contents**\n" + "\n".join(entries)

            if operation == "clear":
                if key == "all":
                    chain["scratchpad"].clear()
                    return "**Scratchpad Cleared**"
                if key in chain["scratchpad"]:
                    del chain["scratchpad"][key]
                    return f"**Removed:** {key}"
                return f"Key '{key}' not found"

            return (
                f"Unknown operation: {operation}. Use: set, get, list, clear"
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in scratchpad: {e}")
            return f"Error in scratchpad: {e}"

    # pylint: disable=too-many-locals
    def assess_reasoning_quality_and_suggest_improvements(
        self, agent_or_team: Any
    ) -> str:
        """Assess reasoning quality and suggest improvements."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" not in session_state:
                return "No active reasoning chain to evaluate."

            chain = session_state["reasoning_chain"]

            # Calculate quality metrics
            steps_count = len(chain["steps"])
            reflections_count = len(chain["reflections"])

            if chain["confidence_trajectory"]:
                avg_confidence = sum(chain["confidence_trajectory"]) / len(
                    chain["confidence_trajectory"]
                )
            else:
                avg_confidence = 0.0

            # Quality assessment
            target_steps = max(1, self.reasoning_depth)
            depth_progress = min(1.0, steps_count / target_steps)
            depth_score = depth_progress * 5.0
            reflection_score = min(5.0, reflections_count * 2.0)
            confidence_score = avg_confidence * 5.0
            diversity_score = min(
                5.0,
                len(set(step["cognitive_mode"] for step in chain["steps"]))
                * 1.5,
            )

            overall_score = (
                depth_score
                + reflection_score
                + confidence_score
                + diversity_score
            ) / 4

            # Generate suggestions
            suggestions = []
            target_steps = max(1, self.reasoning_depth)
            if steps_count < target_steps:
                suggestions.append(
                    f"Add more reasoning steps for deeper analysis (target: {target_steps})"
                )
            if reflections_count == 0:
                suggestions.append("Add reflections to improve meta-cognition")
            if avg_confidence < 0.6:
                suggestions.append(
                    "Consider gathering more evidence or alternative approaches"
                )
            if diversity_score < 3:
                suggestions.append(
                    "Try different cognitive modes (analysis, synthesis, evaluation)"
                )

            result = "**Quality Assessment**\n"
            result += f"**Overall Score:** {overall_score:.1f}/5.0\n\n"
            result += "**Dimensions:**\n"
            result += f"• **Depth:** {depth_score:.1f}/5.0 ({steps_count}/{target_steps} steps)\n"
            result += (
                f"• **Reflection:** {reflection_score:.1f}/5.0 "
                f"({reflections_count} reflections)\n"
            )
            result += f"• **Confidence:** {confidence_score:.1f}/5.0 (avg: {avg_confidence:.1f})\n"
            result += f"• **Diversity:** {diversity_score:.1f}/5.0\n"

            if suggestions:
                result += "\n**Suggestions:**\n"
                for suggestion in suggestions:
                    result += f"• {suggestion}\n"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in quality_check: {e}")
            return f"Error in quality assessment: {e}"

    def retrieve_current_reasoning_session_state(
        self, agent_or_team: Any
    ) -> str:
        """Get current reasoning session state and history."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" not in session_state:
                return "No active reasoning chain."

            chain = session_state["reasoning_chain"]

            result = "**Reasoning Session State**\n"
            result += f"**Chain ID:** {chain['id']}\n"
            result += f"**Steps:** {len(chain['steps'])}\n"
            result += f"**Reflections:** {len(chain['reflections'])}\n"
            result += f"**Scratchpad Items:** {len(chain['scratchpad'])}\n"

            if chain["confidence_trajectory"]:
                avg_conf = sum(chain["confidence_trajectory"]) / len(
                    chain["confidence_trajectory"]
                )
                result += f"**Average Confidence:** {avg_conf:.1f}/1.0\n"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in get_reasoning_state: {e}")
            return f"Error getting state: {e}"

    def synthesize_reasoning_chain_into_conclusion_or_insight(
        self, agent_or_team: Any, synthesis_type: str = "conclusion"
    ) -> str:
        """Combine reasoning chain into insights or conclusions."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" not in session_state:
                return "No active reasoning chain to synthesize."

            chain = session_state["reasoning_chain"]

            if not chain["steps"]:
                return "No reasoning steps to synthesize."

            # Generate synthesis
            if synthesis_type == "summary":
                synthesis = (
                    f"Completed {len(chain['steps'])} reasoning steps with "
                    f"{len(chain['reflections'])} reflections."
                )
            elif synthesis_type == "insights":
                avg_conf = (
                    sum(chain["confidence_trajectory"])
                    / len(chain["confidence_trajectory"])
                    if chain["confidence_trajectory"]
                    else 0
                )
                modes_used = len(
                    set(s["cognitive_mode"] for s in chain["steps"])
                )
                synthesis = (
                    f"Key insight: Reasoning progressed with confidence "
                    f"{avg_conf:.1f}. Used {modes_used} cognitive modes."
                )
            else:
                synthesis = (
                    "Conclusion: Systematic reasoning analysis completed with "
                    "meta-cognitive reflection."
                )

            # Mark chain as completed
            chain["completed_at"] = datetime.now().isoformat()

            result = f"**{synthesis_type.title()} Synthesis**\n"
            result += f"**Chain ID:** {chain['id']}\n"
            result += f"**Steps Processed:** {len(chain['steps'])}\n"
            result += f"**Reflections:** {len(chain['reflections'])}\n\n"
            result += f"**{synthesis_type.title()}:**\n{synthesis}"

            return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in synthesize_reasoning: {e}")
            return f"Error in synthesis: {e}"

    def reset_reasoning_session_state(self, agent_or_team: Any) -> str:
        """Clear current reasoning session state."""
        try:
            session_state = self._get_session_state(agent_or_team)

            if "reasoning_chain" in session_state:
                del session_state["reasoning_chain"]
                return "**Reasoning session cleared** - Ready for new reasoning chain"
            return "No active reasoning session to clear"

        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error in clear_reasoning_session: {e}")
            return f"Error clearing session: {e}"

    # Helper methods
    def _get_session_state(self, agent_or_team: Any) -> dict:
        """Get or create session state for agent/team."""
        # pylint: disable=protected-access
        if not hasattr(agent_or_team, "_reasoning_session_state"):
            agent_or_team._reasoning_session_state = {}
        return agent_or_team._reasoning_session_state

    def _generate_id(self) -> str:
        """Generate unique chain ID."""
        return hashlib.md5(
            f"{datetime.now().isoformat()}_{hash(self)}".encode()
        ).hexdigest()[:8]

    def _detect_biases_in_content(
        self, content: str, evidence: List[str]
    ) -> List[str]:
        """Detect cognitive biases in reasoning content."""
        detected = []

        # Include evidence in the scan so the argument is meaningful and
        # bias markers contained in evidence are also detected.
        combined_text = " ".join([content, *[e for e in evidence if e]])
        content_lower = combined_text.lower()

        for bias_type, patterns in self.bias_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                detected.append(bias_type)

        return detected
