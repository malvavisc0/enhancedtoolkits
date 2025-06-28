"""
Enhanced Universal Reasoning Tools v5.0

A simplified, LLM-optimized reasoning toolkit that combines:
- Multi-modal reasoning with string-based types
- Meta-cognitive capabilities (reflection, working memory)
- Tool planning and orchestration integration
- Bias detection with iterative correction
- Flexible cognitive modes and quality assessment

Author: malvavisc0
License: MIT
Version: 5.0.0
"""

import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

from agno.utils.log import log_debug, log_error

from .base import StrictToolkit


# String constants replacing Enums
REASONING_TYPES = ["deductive", "inductive", "abductive", "causal", "probabilistic", "analogical"]
COGNITIVE_MODES = ["analysis", "synthesis", "evaluation", "planning", "creative", "reflection"]
MAJOR_BIASES = ["confirmation_bias", "anchoring_bias", "overconfidence_bias", "availability_heuristic"]


class EnhancedReasoningTools(StrictToolkit):
    """Enhanced Universal Reasoning Tools v5.0 - LLM-optimized with meta-cognition and tool integration"""

    def __init__(
        self,
        reasoning_depth: int = 5,
        enable_bias_detection: bool = True,
        add_instructions: bool = True,
        **kwargs,
    ):
        self.instructions = """
<reasoning_instructions>
*** Reasoning Tools Instructions ***

### Core Reasoning
**add_structured_reasoning_step** - Add structured reasoning step with cognitive mode
- Modes: analysis, synthesis, evaluation, planning, creative, reflection
- Types: deductive, inductive, abductive, causal, probabilistic, analogical
- Example: `add_structured_reasoning_step(agent, "What causes air pollution?", "analysis", "deductive")`

**apply_multiple_reasoning_types_and_integrate** - Apply multiple reasoning approaches and integrate insights
- Example: `apply_multiple_reasoning_types_and_integrate(agent, "Should we invest?", ["deductive", "probabilistic"])`

**perform_iterative_reasoning_with_bias_correction** - Iterative reasoning with bias correction
- Example: `perform_iterative_reasoning_with_bias_correction(agent, "Is this conclusion valid?", "deductive", max_iterations=3)`

### Meta-Cognition
**add_meta_cognitive_reflection** - Add self-reflection on reasoning process
- Example: `add_meta_cognitive_reflection(agent, "What assumptions am I making?")`

**manage_working_memory_scratchpad** - Working memory for intermediate thoughts
- Operations: set, get, list, clear
- Example: `manage_working_memory_scratchpad(agent, "key_insight", "Market volatility is increasing", "set")`

**assess_reasoning_quality_and_suggest_improvements** - Assess reasoning quality and suggest improvements
- Example: `assess_reasoning_quality_and_suggest_improvements(agent)`

### Tool Integration
**create_reasoning_and_tool_execution_plan** - Plan sequence of reasoning and tool steps
- Example: `create_reasoning_and_tool_execution_plan(agent, "Analyze market data", ["read_file", "add_structured_reasoning_step"])`

**execute_and_monitor_reasoning_tool_plan** - Execute planned reasoning workflow
- Actions: execute, status, complete_step
- Example: `execute_and_monitor_reasoning_tool_plan(agent, "execute")`

### Session Management
**retrieve_current_reasoning_session_state** - Get current session state and history
**synthesize_reasoning_chain_into_conclusion_or_insight** - Combine reasoning into conclusions or insights
**reset_reasoning_session_state** - Reset session state

### Workflow Example
1. add_structured_reasoning_step(agent, "Problem analysis", "analysis", "deductive")
2. manage_working_memory_scratchpad(agent, "key_facts", "Important data points", "set")
3. add_meta_cognitive_reflection(agent, "Are there alternative explanations?")
4. assess_reasoning_quality_and_suggest_improvements(agent)
5. synthesize_reasoning_chain_into_conclusion_or_insight(agent, "conclusion")
</reasoning_instructions>
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
            "confirmation_bias": ["confirms", "supports", "validates", "proves", "obviously", "clearly"],
            "anchoring_bias": ["first", "initial", "starting", "baseline", "reference"],
            "availability_heuristic": ["recent", "memorable", "vivid", "comes to mind", "recall"],
            "overconfidence_bias": ["definitely", "certainly", "absolutely", "guaranteed", "impossible"],
        }

        # Cognitive scaffolding prompts
        self.cognitive_prompts = {
            "analysis": "Break this down: What are the key components? How do they relate?",
            "synthesis": "Combine insights: What patterns emerge? How do pieces fit together?",
            "evaluation": "Assess critically: What are strengths/weaknesses? What's missing?",
            "planning": "Think ahead: What steps are needed? What could go wrong?",
            "creative": "Think differently: What alternatives exist? What if we changed X?",
            "reflection": "Think about thinking: How did I approach this? What assumptions did I make?",
        }

        # Register tools
        self.register(self.add_structured_reasoning_step)
        self.register(self.apply_multiple_reasoning_types_and_integrate)
        self.register(self.perform_iterative_reasoning_with_bias_correction)
        self.register(self.add_meta_cognitive_reflection)
        self.register(self.manage_working_memory_scratchpad)
        self.register(self.assess_reasoning_quality_and_suggest_improvements)
        self.register(self.create_reasoning_and_tool_execution_plan)
        self.register(self.execute_and_monitor_reasoning_tool_plan)
        self.register(self.retrieve_current_reasoning_session_state)
        self.register(self.synthesize_reasoning_chain_into_conclusion_or_insight)
        self.register(self.reset_reasoning_session_state)

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

            log_debug(f"Reasoning step ({cognitive_mode}/{reasoning_type}): {problem[:50]}...")

            session_state = self._get_session_state(agent_or_team)
            
            # Initialize session if needed
            if "reasoning_chain" not in session_state:
                session_state["reasoning_chain"] = {
                    "id": self._generate_id(),
                    "steps": [],
                    "reflections": [],
                    "scratchpad": {},
                    "tool_plan": [],
                    "created_at": datetime.now().isoformat(),
                    "confidence_trajectory": [],
                }

            chain = session_state["reasoning_chain"]

            # Detect biases if enabled
            biases_detected = []
            if self.enable_bias_detection:
                biases_detected = self._detect_biases_in_content(problem, evidence or [])

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

            # Get cognitive scaffolding
            scaffolding = self.cognitive_prompts.get(cognitive_mode, "Think step by step:")

            result = f"**Step {step['id']}: {cognitive_mode.title()} ({reasoning_type})**\n"
            result += f"**Problem:** {problem}\n"
            result += f"**Confidence:** {confidence:.1f}/1.0\n"
            result += f"**Scaffolding:** {scaffolding}\n"

            if evidence:
                result += f"**Evidence:** {len(evidence)} items\n"

            if biases_detected:
                bias_names = [b.replace("_", " ").title() for b in biases_detected]
                result += f"**Biases Detected:** {', '.join(bias_names)}\n"

            if confidence < 0.7:
                result += "**Low Confidence** - Consider reflection or quality check\n"

            return result

        except Exception as e:
            log_error(f"Error in reason_step: {e}")
            return f"Error in reasoning step: {e}"

    def apply_multiple_reasoning_types_and_integrate(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_types: Optional[List[str]] = None,
        evidence: Optional[List[str]] = None,
    ) -> str:
        """Apply multiple reasoning approaches and integrate insights."""
        try:
            if not reasoning_types:
                reasoning_types = ["deductive", "inductive"]

            # Validate reasoning types
            valid_types = [rt for rt in reasoning_types if rt in REASONING_TYPES]
            if not valid_types:
                valid_types = ["deductive"]

            log_debug(f"Multi-modal reasoning with {len(valid_types)} approaches: {problem[:50]}...")

            session_state = self._get_session_state(agent_or_team)
            
            results = []
            for reasoning_type in valid_types:
                # Apply each reasoning type
                step_result = self.add_structured_reasoning_step(
                    agent_or_team, problem, "analysis", reasoning_type, evidence, 0.6
                )
                results.append(f"**{reasoning_type.title()} Approach:**\n{step_result}")

            # Calculate overall confidence
            chain = session_state.get("reasoning_chain", {})
            if chain.get("confidence_trajectory"):
                avg_confidence = sum(chain["confidence_trajectory"]) / len(chain["confidence_trajectory"])
            else:
                avg_confidence = 0.6

            integration = f"\n**Multi-Modal Integration:**\n"
            integration += f"Applied {len(valid_types)} reasoning approaches\n"
            integration += f"Overall confidence: {avg_confidence:.1f}/1.0\n"
            integration += "Consider synthesis to combine insights"

            return "\n\n".join(results) + "\n" + integration

        except Exception as e:
            log_error(f"Error in multi_modal_reason: {e}")
            return f"Error in multi-modal reasoning: {e}"

    def perform_iterative_reasoning_with_bias_correction(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_type: str = "deductive",
        evidence: Optional[List[str]] = None,
        max_iterations: int = 3,
    ) -> str:
        """Iterative reasoning with bias detection and correction."""
        try:
            log_debug(f"Starting iterative reasoning: {problem[:50]}...")

            history = []
            current_problem = problem
            iteration = 0
            last_biases = []

            while iteration < max_iterations:
                # Generate reasoning step
                if iteration == 0:
                    prompt = current_problem
                else:
                    bias_text = ", ".join([b.replace("_", " ").title() for b in last_biases])
                    prompt = f"Previous reasoning had bias: {bias_text}. Revise by addressing this bias: {current_problem}"

                step_result = self.add_structured_reasoning_step(agent_or_team, prompt, "evaluation", reasoning_type, evidence, 0.7)

                # Detect biases
                detected_biases = []
                if self.enable_bias_detection:
                    detected_biases = self._detect_biases_in_content(prompt, evidence or [])

                history.append({
                    "iteration": iteration + 1,
                    "result": step_result,
                    "biases": detected_biases,
                })

                # Check for major biases
                major_found = [b for b in detected_biases if b in MAJOR_BIASES]
                if not major_found:
                    break

                last_biases = major_found
                iteration += 1

            # Format output
            output_parts = []
            for step in history:
                output_parts.append(f"**Iteration {step['iteration']}:**\n{step['result']}")
                if step["biases"]:
                    bias_names = [b.replace("_", " ").title() for b in step["biases"]]
                    output_parts.append(f"Biases detected: {', '.join(bias_names)}")

            if last_biases and iteration == max_iterations:
                output_parts.append("Maximum iterations reached. Manual review recommended.")
            else:
                output_parts.append("Reasoning completed with bias mitigation.")

            return "\n\n".join(output_parts)

        except Exception as e:
            log_error(f"Error in iterative_reason: {e}")
            return f"Error in iterative reasoning: {e}"

    def add_meta_cognitive_reflection(self, agent_or_team: Any, reflection: str, step_id: Optional[int] = None) -> str:
        """Add meta-cognitive reflection to current reasoning chain."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" not in session_state:
                return "No active reasoning chain. Start with add_structured_reasoning_step first."
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
                insight = "Good - questioning assumptions strengthens reasoning"
            elif "bias" in reflection.lower():
                insight = "Excellent - bias awareness improves objectivity"
            elif "alternative" in reflection.lower():
                insight = "Strong - considering alternatives enhances robustness"

            result = f"**Meta-Cognitive Reflection**\n"
            result += f"**Reflection:** {reflection}\n"
            if step_id:
                result += f"**Reflecting on Step:** {step_id}\n"
            result += f"**Insight:** {insight}\n"
            result += f"**Total Reflections:** {len(chain['reflections'])}"

            return result

        except Exception as e:
            log_error(f"Error in reflect: {e}")
            return f"Error in reflection: {e}"

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
                return "No active reasoning chain. Start with reason_step first."

            chain = session_state["reasoning_chain"]

            if operation == "set":
                if value is None:
                    return "Value required for set operation"
                chain["scratchpad"][key] = {
                    "value": value,
                    "updated_at": datetime.now().isoformat()
                }
                return f"**Scratchpad Updated**\n**{key}:** {value}"

            elif operation == "get":
                if key in chain["scratchpad"]:
                    entry = chain["scratchpad"][key]
                    return f"**Scratchpad Entry**\n**{key}:** {entry['value']}\n**Updated:** {entry['updated_at']}"
                else:
                    return f"Key '{key}' not found in scratchpad"

            elif operation == "list":
                if not chain["scratchpad"]:
                    return "**Scratchpad Empty**"
                entries = [f"• **{k}:** {v['value']}" for k, v in chain["scratchpad"].items()]
                return f"**Scratchpad Contents**\n" + "\n".join(entries)

            elif operation == "clear":
                if key == "all":
                    chain["scratchpad"].clear()
                    return "**Scratchpad Cleared**"
                elif key in chain["scratchpad"]:
                    del chain["scratchpad"][key]
                    return f"**Removed:** {key}"
                else:
                    return f"Key '{key}' not found"

            else:
                return f"Unknown operation: {operation}. Use: set, get, list, clear"

        except Exception as e:
            log_error(f"Error in scratchpad: {e}")
            return f"Error in scratchpad: {e}"

    def assess_reasoning_quality_and_suggest_improvements(self, agent_or_team: Any) -> str:
        """Assess reasoning quality and suggest improvements."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" not in session_state:
                return "No active reasoning chain to evaluate."

            chain = session_state["reasoning_chain"]
            
            # Calculate quality metrics
            steps_count = len(chain["steps"])
            reflections_count = len(chain["reflections"])
            scratchpad_items = len(chain["scratchpad"])
            
            if chain["confidence_trajectory"]:
                avg_confidence = sum(chain["confidence_trajectory"]) / len(chain["confidence_trajectory"])
            else:
                avg_confidence = 0.0

            # Quality assessment
            depth_score = min(5.0, steps_count * 1.0)
            reflection_score = min(5.0, reflections_count * 2.0)
            confidence_score = avg_confidence * 5.0
            diversity_score = min(5.0, len(set(step["cognitive_mode"] for step in chain["steps"])) * 1.5)
            
            overall_score = (depth_score + reflection_score + confidence_score + diversity_score) / 4

            # Generate suggestions
            suggestions = []
            if steps_count < 3:
                suggestions.append("Add more reasoning steps for deeper analysis")
            if reflections_count == 0:
                suggestions.append("Add reflections to improve meta-cognition")
            if avg_confidence < 0.6:
                suggestions.append("Consider gathering more evidence or alternative approaches")
            if diversity_score < 3:
                suggestions.append("Try different cognitive modes (analysis, synthesis, evaluation)")

            result = f"**Quality Assessment**\n"
            result += f"**Overall Score:** {overall_score:.1f}/5.0\n\n"
            result += f"**Dimensions:**\n"
            result += f"• **Depth:** {depth_score:.1f}/5.0 ({steps_count} steps)\n"
            result += f"• **Reflection:** {reflection_score:.1f}/5.0 ({reflections_count} reflections)\n"
            result += f"• **Confidence:** {confidence_score:.1f}/5.0 (avg: {avg_confidence:.1f})\n"
            result += f"• **Diversity:** {diversity_score:.1f}/5.0\n"

            if suggestions:
                result += f"\n**Suggestions:**\n"
                for suggestion in suggestions:
                    result += f"• {suggestion}\n"

            return result

        except Exception as e:
            log_error(f"Error in quality_check: {e}")
            return f"Error in quality assessment: {e}"

    def create_reasoning_and_tool_execution_plan(
        self,
        agent_or_team: Any,
        task: str,
        available_tools: List[str],
        context: Optional[str] = None,
    ) -> str:
        """Plan sequence of reasoning and tool steps for complex tasks."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" not in session_state:
                return "Start with reason_step first to establish reasoning context."

            chain = session_state["reasoning_chain"]

            # Generate tool plan
            plan = []
            
            # Step 1: Analysis
            plan.append({
                "type": "reasoning",
                "tool": "reason_step",
                "purpose": f"Analyze task: {task}",
                "inputs": {"cognitive_mode": "analysis", "reasoning_type": "deductive"},
                "dependencies": [],
            })

            # Step 2: Information gathering (if applicable tools available)
            info_tools = [t for t in available_tools if t in ["read_file", "list_files", "search_files"]]
            if info_tools:
                plan.append({
                    "type": "tool",
                    "tool": info_tools[0],
                    "purpose": f"Gather information for: {task}",
                    "inputs": {"context_hint": context or "Specify based on task"},
                    "dependencies": ["add_structured_reasoning_step"],
                })

            # Step 3: Synthesis
            plan.append({
                "type": "reasoning",
                "tool": "add_structured_reasoning_step",
                "purpose": f"Synthesize insights for: {task}",
                "inputs": {"cognitive_mode": "synthesis", "reasoning_type": "inductive"},
                "dependencies": info_tools[:1] if info_tools else ["add_structured_reasoning_step"],
            })

            # Store plan
            chain["tool_plan"] = plan

            result = f"**Reasoning-Tool Plan Created**\n"
            result += f"**Task:** {task}\n"
            result += f"**Context:** {context or 'None'}\n"
            result += f"**Planned Steps:** {len(plan)}\n\n"

            for i, step in enumerate(plan, 1):
                deps = f" (depends on: {', '.join(step['dependencies'])})" if step['dependencies'] else ""
                result += f"{i}. **{step['tool']}** ({step['type']}) - {step['purpose']}{deps}\n"

            result += f"\n**Next:** Use orchestrate_reasoning(agent, 'execute') to run the plan"

            return result

        except Exception as e:
            log_error(f"Error in plan_reasoning_tools: {e}")
            return f"Error in tool planning: {e}"

    def execute_and_monitor_reasoning_tool_plan(self, agent_or_team: Any, action: str = "execute") -> str:
        """Execute and monitor reasoning-tool workflow."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" not in session_state:
                return "No active reasoning chain with tool plan."

            chain = session_state["reasoning_chain"]
            
            if not chain.get("tool_plan"):
                return "No tool plan found. Use plan_reasoning_tools first."

            if action == "execute":
                # Find next ready step
                for step in chain["tool_plan"]:
                    if step.get("status") != "completed" and self._dependencies_met(step, chain["tool_plan"]):
                        step["status"] = "ready"
                        return f"**Ready to Execute**\n**Tool:** {step['tool']}\n**Purpose:** {step['purpose']}\n**Type:** {step['type']}\n**Inputs:** {step['inputs']}\n\n**Action Required:** Execute this step, then call orchestrate_reasoning again"

                return "**Plan Complete** - All steps finished"

            elif action == "status":
                completed = len([s for s in chain["tool_plan"] if s.get("status") == "completed"])
                return f"**Plan Status:** {completed}/{len(chain['tool_plan'])} steps completed"

            elif action == "complete_step":
                ready_steps = [s for s in chain["tool_plan"] if s.get("status") == "ready"]
                if ready_steps:
                    ready_steps[0]["status"] = "completed"
                    return "**Step Completed** - Call orchestrate_reasoning('execute') for next step"
                return "No ready steps to complete"

            else:
                return f"Unknown action: {action}. Use: execute, status, complete_step"

        except Exception as e:
            log_error(f"Error in orchestrate_reasoning: {e}")
            return f"Error in orchestration: {e}"

    def retrieve_current_reasoning_session_state(self, agent_or_team: Any) -> str:
        """Get current reasoning session state and history."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" not in session_state:
                return "No active reasoning chain."

            chain = session_state["reasoning_chain"]
            
            result = f"**Reasoning Session State**\n"
            result += f"**Chain ID:** {chain['id']}\n"
            result += f"**Steps:** {len(chain['steps'])}\n"
            result += f"**Reflections:** {len(chain['reflections'])}\n"
            result += f"**Scratchpad Items:** {len(chain['scratchpad'])}\n"
            result += f"**Tool Plan Steps:** {len(chain.get('tool_plan', []))}\n"
            
            if chain["confidence_trajectory"]:
                avg_conf = sum(chain["confidence_trajectory"]) / len(chain["confidence_trajectory"])
                result += f"**Average Confidence:** {avg_conf:.1f}/1.0\n"

            return result

        except Exception as e:
            log_error(f"Error in get_reasoning_state: {e}")
            return f"Error getting state: {e}"

    def synthesize_reasoning_chain_into_conclusion_or_insight(self, agent_or_team: Any, synthesis_type: str = "conclusion") -> str:
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
                synthesis = f"Completed {len(chain['steps'])} reasoning steps with {len(chain['reflections'])} reflections."
            elif synthesis_type == "insights":
                avg_conf = sum(chain["confidence_trajectory"]) / len(chain["confidence_trajectory"]) if chain["confidence_trajectory"] else 0
                synthesis = f"Key insight: Reasoning progressed with confidence {avg_conf:.1f}. Used {len(set(s['cognitive_mode'] for s in chain['steps']))} cognitive modes."
            else:
                synthesis = f"Conclusion: Systematic reasoning analysis completed with meta-cognitive reflection."

            # Mark chain as completed
            chain["completed_at"] = datetime.now().isoformat()

            result = f"**{synthesis_type.title()} Synthesis**\n"
            result += f"**Chain ID:** {chain['id']}\n"
            result += f"**Steps Processed:** {len(chain['steps'])}\n"
            result += f"**Reflections:** {len(chain['reflections'])}\n\n"
            result += f"**{synthesis_type.title()}:**\n{synthesis}"

            return result

        except Exception as e:
            log_error(f"Error in synthesize_reasoning: {e}")
            return f"Error in synthesis: {e}"

    def reset_reasoning_session_state(self, agent_or_team: Any) -> str:
        """Clear current reasoning session state."""
        try:
            session_state = self._get_session_state(agent_or_team)
            
            if "reasoning_chain" in session_state:
                del session_state["reasoning_chain"]
                return "**Reasoning session cleared** - Ready for new reasoning chain"
            else:
                return "No active reasoning session to clear"

        except Exception as e:
            log_error(f"Error in clear_reasoning_session: {e}")
            return f"Error clearing session: {e}"

    # Helper methods
    def _get_session_state(self, agent_or_team: Any) -> dict:
        """Get or create session state for agent/team."""
        if not hasattr(agent_or_team, "_reasoning_session_state"):
            agent_or_team._reasoning_session_state = {}
        return agent_or_team._reasoning_session_state

    def _generate_id(self) -> str:
        """Generate unique chain ID."""
        return hashlib.md5(f"{datetime.now().isoformat()}_{hash(self)}".encode()).hexdigest()[:8]

    def _detect_biases_in_content(self, content: str, evidence: List[str]) -> List[str]:
        """Detect cognitive biases in reasoning content."""
        detected = []
        content_lower = content.lower()
        
        for bias_type, patterns in self.bias_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                detected.append(bias_type)
        
        return detected

    def _dependencies_met(self, step: Dict[str, Any], plan: List[Dict[str, Any]]) -> bool:
        """Check if step dependencies are met."""
        if not step.get("dependencies"):
            return True
        
        for dep in step["dependencies"]:
            dep_steps = [s for s in plan if s["tool"] == dep]
            if not dep_steps or dep_steps[0].get("status") != "completed":
                return False
        
        return True
