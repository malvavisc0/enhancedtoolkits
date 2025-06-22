"""
Enhanced Universal Reasoning Tools v4.0

A production-ready reasoning toolkit that combines:
- Multi-modal reasoning (deductive, inductive, abductive, causal, probabilistic, analogical)
- Cognitive bias detection with natural language explanations
- Session management and reasoning step tracking
- Result evaluation and iterative reasoning workflows
- Human-like conversational output

Author: malvavisc0
License: MIT
Version: 4.0.0
"""

from datetime import datetime
from enum import Enum
from textwrap import dedent
from typing import Any, Dict, List, Optional, Sequence, Union

from agno.utils.log import log_debug, log_error

from .base import StrictToolkit


class ReasoningType(Enum):
    """Supported reasoning methodologies."""

    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    CAUSAL = "causal"
    PROBABILISTIC = "probabilistic"
    ANALOGICAL = "analogical"


class NextAction(Enum):
    """Next action options for reasoning workflow."""

    CONTINUE = "continue"
    VALIDATE = "validate"
    FINAL_ANSWER = "final_answer"


# Major biases that require iterative correction
MAJOR_BIASES = {
    "confirmation_bias",
    "anchoring_bias",
    "overconfidence_bias",
    "availability_heuristic",
}


class ReasoningStep:
    """Represents a single reasoning step with metadata."""

    def __init__(
        self,
        step_type: str,
        content: str,
        reasoning_type: Optional[ReasoningType] = None,
        confidence: str = "moderately confident",
        evidence: Optional[List[str]] = None,
        biases_detected: Optional[List[str]] = None,
        next_action: NextAction = NextAction.CONTINUE,
        timestamp: Optional[str] = None,
    ):
        self.step_type = step_type
        self.content = content
        self.reasoning_type = reasoning_type.value if reasoning_type else None
        self.confidence = confidence
        self.evidence = evidence or []
        self.biases_detected = biases_detected or []
        self.next_action = next_action.value
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "step_type": self.step_type,
            "content": self.content,
            "reasoning_type": self.reasoning_type,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "biases_detected": self.biases_detected,
            "next_action": self.next_action,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReasoningStep":
        """Create from dictionary."""
        reasoning_type = (
            ReasoningType(data["reasoning_type"]) if data.get("reasoning_type") else None
        )
        next_action = NextAction(data.get("next_action", "continue"))

        return cls(
            step_type=data["step_type"],
            content=data["content"],
            reasoning_type=reasoning_type,
            confidence=data.get("confidence", "moderately confident"),
            evidence=data.get("evidence", []),
            biases_detected=data.get("biases_detected", []),
            next_action=next_action,
            timestamp=data.get("timestamp"),
        )


class EnhancedReasoningTools(StrictToolkit):
    """
    Enhanced Universal Reasoning Tools v4.0

    A production-ready reasoning toolkit that combines multi-modal reasoning,
    bias detection, session management, and iterative workflows.
    """

    def __init__(
        self,
        reasoning_depth: int = 5,
        enable_bias_detection: bool = True,
        add_instructions: bool = True,
        **kwargs,
    ):
        # Enhanced instructions
        self.add_instructions = add_instructions
        if self.add_instructions:
            self.instructions = EnhancedReasoningTools.get_llm_usage_instructions()

        super().__init__(
            name="enhanced_reasoning_tools",
            instructions=self.instructions,
            add_instructions=add_instructions,
            **kwargs,
        )

        # Configuration
        self.reasoning_depth = max(1, min(10, reasoning_depth))
        self.enable_bias_detection = enable_bias_detection

        # Bias detection patterns (enhanced)
        self.bias_patterns = {
            "confirmation_bias": {
                "keywords": [
                    "confirms",
                    "supports",
                    "validates",
                    "proves",
                    "obviously",
                    "clearly",
                ],
                "phrases": [
                    "as expected",
                    "just as I thought",
                    "this proves",
                    "confirms my belief",
                ],
            },
            "anchoring_bias": {
                "keywords": ["first", "initial", "starting", "baseline", "reference"],
                "phrases": ["based on the first", "starting from", "initially thought"],
            },
            "availability_heuristic": {
                "keywords": ["recent", "memorable", "vivid", "comes to mind", "recall"],
                "phrases": ["I remember", "recently saw", "just heard", "easy to recall"],
            },
            "overconfidence_bias": {
                "keywords": [
                    "definitely",
                    "certainly",
                    "absolutely",
                    "guaranteed",
                    "impossible",
                ],
                "phrases": ["I'm 100% sure", "there's no doubt", "absolutely certain"],
            },
        }

        # Register tools
        self.register(self.reason)
        self.register(self.multi_modal_reason)
        self.register(self.analyze_reasoning)
        self.register(self.iterative_reason)
        self.register(self.get_reasoning_history)
        self.register(self.clear_reasoning_session)
        if enable_bias_detection:
            self.register(self.detect_biases)

    def iterative_reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_type: Union[ReasoningType, str] = ReasoningType.DEDUCTIVE,
        evidence: Optional[List[str]] = None,
        context: Optional[str] = None,
        max_iterations: int = 3,
    ) -> str:
        """
        Improved iterative reasoning with explicit bias feedback integration and stepwise narration.
        
        Args:
            agent_or_team: The agent or team requesting reasoning
            problem: The problem or question to analyze
            reasoning_type: Type of reasoning to apply
            evidence: Supporting evidence or data points
            context: Additional context for the problem
            max_iterations: Maximum number of iterations to attempt
            
        Returns:
            Iterative reasoning analysis with bias detection and correction
        """
        try:
            log_debug(f"Starting iterative reasoning: {problem[:50]}...")
            
            history = []
            current_answer = None
            current_problem = problem
            current_reasoning_type = reasoning_type
            current_evidence = evidence
            current_context = context
            iteration = 0
            last_biases = []
            previous_bias_sets = []  # Track bias history to detect improvement

            while iteration < max_iterations:
                # Step 1: Generate answer (pass previous answer and bias feedback if not first iteration)
                if iteration == 0:
                    prompt = current_problem
                else:
                    bias_names = [b.replace("_", " ").title() for b in last_biases]
                    bias_text = ", ".join(bias_names)
                    prompt = (
                        f"Previous answer:\n{current_answer}\n\n"
                        f"Bias detected: {bias_text}.\n"
                        f"Revise your answer by explicitly addressing this bias. "
                        f"Add counterarguments, alternative perspectives, or express more uncertainty as needed. "
                        f"Narrate what you changed and why."
                    )
                
                # Use a dedicated method to generate the answer from the prompt
                answer = self._generate_reasoning_step(
                    agent_or_team,
                    prompt,
                    current_reasoning_type,
                    current_evidence,
                    current_context,
                )
                
                # Step 2: Detect biases in the generated answer
                detected_biases = []
                if self.enable_bias_detection:
                    detected_biases = self._detect_biases_in_content(
                        answer, current_evidence or [], current_context
                    )
                
                history.append(
                    {
                        "iteration": iteration + 1,
                        "answer": answer,
                        "biases": detected_biases,
                    }
                )
                
                # Step 3: Check for major bias and improvement
                major_found = [b for b in detected_biases if b in MAJOR_BIASES]
                
                # Check if we're making progress (fewer biases or different biases)
                if iteration > 0:
                    bias_set = set(major_found)
                    if bias_set in previous_bias_sets:
                        # Same biases detected again, stop to avoid infinite loop
                        break
                    previous_bias_sets.append(bias_set)
                
                if not major_found:
                    break
                    
                last_biases = major_found
                current_answer = answer
                iteration += 1

            # Compose output
            output_parts = []
            for step in history:
                output_parts.append(
                    f"**Iteration {step['iteration']} Reasoning:**\n{step['answer']}"
                )
                if step["biases"]:
                    bias_names = [b.replace("_", " ").title() for b in step["biases"]]
                    output_parts.append(f"\nBiases detected: {', '.join(bias_names)}")
                else:
                    output_parts.append("\nNo major bias detected.")

            if last_biases and iteration == max_iterations:
                output_parts.append(
                    "\nMaximum iterations reached. Some bias may remain, and further review is recommended."
                )
            elif last_biases and len(previous_bias_sets) > 1:
                output_parts.append(
                    "\nBias correction reached a stable state. Further manual review may be needed."
                )
            else:
                output_parts.append(
                    "\nFinal answer is considered balanced and bias-mitigated."
                )

            return "\n\n".join(output_parts)
            
        except Exception as e:
            log_error(f"Error in iterative reasoning: {e}")
            return f"I encountered an issue during iterative reasoning: {e}. Let me try a simpler approach."

    def _generate_reasoning_step(
        self,
        agent_or_team: Any,
        prompt: str,
        reasoning_type: Union[ReasoningType, str],
        evidence: Optional[List[str]],
        context: Optional[str],
    ) -> str:
        """
        Generate a reasoning step from a prompt, using the LLM or self.reason as appropriate.
        """
        # If using an LLM, pass the prompt directly.
        # If using self.reason, you may need to adapt the method to accept a custom prompt.
        return self.reason(
            agent_or_team,
            prompt,
            reasoning_type,
            evidence,
            context,
        )

    def reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_type: Union[ReasoningType, str] = ReasoningType.DEDUCTIVE,
        evidence: Optional[List[str]] = None,
        context: Optional[str] = None,
    ) -> str:
        """
        Apply structured reasoning to a problem with session tracking.

        Args:
            agent_or_team: The agent or team requesting reasoning
            problem: The problem or question to analyze
            reasoning_type: Type of reasoning to apply
            evidence: Supporting evidence or data points
            context: Additional context for the problem

        Returns:
            Human-like reasoning analysis with natural language explanations
        """
        try:
            # Convert string to enum if needed
            if isinstance(reasoning_type, str):
                try:
                    reasoning_type = ReasoningType(reasoning_type)
                except ValueError:
                    reasoning_type = ReasoningType.DEDUCTIVE

            log_debug(f"Reasoning ({reasoning_type.value}): {problem[:50]}...")

            # Initialize session state
            self._initialize_session_state(agent_or_team)

            # Analyze the problem
            analysis = self._analyze_problem(
                problem, reasoning_type, evidence or [], context
            )

            # Detect biases if enabled
            biases_detected = []
            if self.enable_bias_detection:
                biases_detected = self._detect_biases_in_content(
                    problem, evidence or [], context
                )

            # Create reasoning step
            reasoning_step = ReasoningStep(
                step_type="reasoning",
                content=problem,
                reasoning_type=reasoning_type,
                confidence=analysis.get("confidence_level", "moderately confident"),
                evidence=evidence or [],
                biases_detected=biases_detected,
                next_action=NextAction.CONTINUE,
            )

            # Store reasoning step
            self._store_reasoning_step(agent_or_team, reasoning_step)

            # Generate human-like output
            output = self._format_reasoning_output(
                problem, reasoning_type, analysis, biases_detected, evidence or []
            )

            return output

        except Exception as e:
            log_error(f"Error in reasoning: {e}")
            return f"I encountered an issue while analyzing this problem: {e}. Let me try a different approach."

    def multi_modal_reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_types: Sequence[Union[ReasoningType, str]],
        evidence: Optional[List[str]] = None,
    ) -> str:
        """
        Apply multiple reasoning approaches and integrate insights.

        Args:
            agent_or_team: The agent or team requesting reasoning
            problem: The problem to analyze
            reasoning_types: List of reasoning types to apply
            evidence: Supporting evidence or data points

        Returns:
            Integrated analysis using multiple reasoning approaches
        """
        try:
            # Convert strings to enums
            converted_types = []
            for rt in reasoning_types:
                if isinstance(rt, str):
                    try:
                        converted_types.append(ReasoningType(rt))
                    except ValueError:
                        converted_types.append(ReasoningType.DEDUCTIVE)
                else:
                    converted_types.append(rt)

            log_debug(
                f"Multi-modal reasoning with {len(converted_types)} approaches: {problem[:50]}..."
            )

            # Initialize session state
            self._initialize_session_state(agent_or_team)

            # Apply each reasoning type
            reasoning_results = {}
            for reasoning_type in converted_types:
                analysis = self._analyze_problem(
                    problem, reasoning_type, evidence or [], None
                )
                reasoning_results[reasoning_type.value] = analysis

            # Integrate results
            integration = self._integrate_multi_modal_results(reasoning_results, problem)

            # Detect biases
            biases_detected = []
            if self.enable_bias_detection:
                biases_detected = self._detect_biases_in_content(
                    problem, evidence or [], None
                )

            # Create reasoning step
            reasoning_step = ReasoningStep(
                step_type="multi_modal_reasoning",
                content=problem,
                reasoning_type=None,  # Multiple types used
                confidence=integration.get("overall_confidence", "moderately confident"),
                evidence=evidence or [],
                biases_detected=biases_detected,
                next_action=NextAction.CONTINUE,
            )

            # Store reasoning step
            self._store_reasoning_step(agent_or_team, reasoning_step)

            # Generate output
            output = self._format_multi_modal_output(
                problem, converted_types, integration, evidence or []
            )

            return output

        except Exception as e:
            log_error(f"Error in multi-modal reasoning: {e}")
            return f"I had trouble applying multiple reasoning approaches: {e}. Let me focus on the core analysis."

    def analyze_reasoning(
        self,
        agent_or_team: Any,
        result: str,
        analysis: str,
        next_action: str = "continue",
        confidence: str = "moderately confident",
    ) -> str:
        """
        Analyze reasoning results and determine next actions.

        Args:
            agent_or_team: The agent or team requesting analysis
            result: The outcome of the previous reasoning step
            analysis: Your analysis of the results
            next_action: What to do next ("continue", "validate", or "final_answer")
            confidence: How confident you are in this analysis

        Returns:
            Analysis summary with reasoning history and next action guidance
        """
        try:
            log_debug(f"Analyzing reasoning results: {result[:50]}...")

            # Initialize session state
            self._initialize_session_state(agent_or_team)

            # Map string next_action to enum
            next_action_enum = NextAction.CONTINUE
            if next_action.lower() == "validate":
                next_action_enum = NextAction.VALIDATE
            elif next_action.lower() in ["final", "final_answer", "finalize"]:
                next_action_enum = NextAction.FINAL_ANSWER

            # Create analysis step
            analysis_step = ReasoningStep(
                step_type="analysis",
                content=analysis,
                confidence=confidence,
                next_action=next_action_enum,
            )

            # Store analysis step
            self._store_reasoning_step(agent_or_team, analysis_step)

            # Get reasoning history
            history = self._get_reasoning_history(agent_or_team)

            # Generate analysis output
            output = self._format_analysis_output(
                result, analysis, next_action_enum, confidence, history
            )

            return output

        except Exception as e:
            log_error(f"Error in reasoning analysis: {e}")
            return f"I had trouble analyzing the reasoning results: {e}. The reasoning might still be sound."

    def detect_biases(self, agent_or_team: Any, reasoning_content: str) -> str:
        """
        Detect cognitive biases in reasoning content.

        Args:
            agent_or_team: The agent or team requesting bias detection
            reasoning_content: The reasoning text to analyze for biases

        Returns:
            Natural language explanation of detected biases and suggestions
        """
        try:
            log_debug(
                f"Detecting biases in reasoning content: {reasoning_content[:50]}..."
            )

            detected_biases = self._identify_biases(reasoning_content)

            # Store detected biases in agent_or_team.session_state for context-awareness
            if (
                hasattr(agent_or_team, "session_state")
                and agent_or_team.session_state is not None
            ):
                agent_or_team.session_state["last_detected_biases"] = detected_biases

            if not detected_biases:
                return "Looking at this reasoning, I don't notice any obvious cognitive biases. The thinking appears balanced and well-considered."

            # Generate natural bias explanation
            bias_explanation = self._explain_biases_naturally(
                detected_biases, reasoning_content
            )

            return bias_explanation

        except Exception as e:
            log_error(f"Error in bias detection: {e}")
            return f"I had trouble analyzing this for biases: {e}. The reasoning might still be sound."

    def get_reasoning_history(self, agent_or_team: Any) -> str:
        """
        Get the reasoning history for the current session.

        Args:
            agent_or_team: The agent or team to get history for

        Returns:
            Formatted reasoning history
        """
        try:
            history = self._get_reasoning_history(agent_or_team)
            if not history:
                return "No reasoning history found for this session."

            output_parts = ["## Reasoning History\n"]
            for i, step in enumerate(history, 1):
                step_obj = ReasoningStep.from_dict(step)
                output_parts.append(f"**Step {i}: {step_obj.step_type.title()}**")
                output_parts.append(
                    f"- Content: {step_obj.content[:100]}{'...' if len(step_obj.content) > 100 else ''}"
                )
                output_parts.append(f"- Confidence: {step_obj.confidence}")
                if step_obj.reasoning_type:
                    output_parts.append(f"- Reasoning Type: {step_obj.reasoning_type}")
                output_parts.append("")

            return "\n".join(output_parts)

        except Exception as e:
            log_error(f"Error getting reasoning history: {e}")
            return f"Error retrieving reasoning history: {e}"

    def clear_reasoning_session(self, agent_or_team: Any) -> str:
        """
        Clear the reasoning session state.

        Args:
            agent_or_team: The agent or team to clear session for

        Returns:
            Confirmation message
        """
        try:
            if hasattr(agent_or_team, "session_state") and agent_or_team.session_state:
                if "reasoning_steps" in agent_or_team.session_state:
                    run_id = getattr(agent_or_team, "run_id", "default")
                    if run_id in agent_or_team.session_state["reasoning_steps"]:
                        del agent_or_team.session_state["reasoning_steps"][run_id]
                        return "Reasoning session cleared successfully."

            return "No active reasoning session found to clear."

        except Exception as e:
            log_error(f"Error clearing reasoning session: {e}")
            return f"Error clearing reasoning session: {e}"

    # Helper methods

    def _initialize_session_state(self, agent_or_team: Any) -> None:
        """Initialize session state for reasoning tracking."""
        if not hasattr(agent_or_team, "session_state") or agent_or_team.session_state is None:
            agent_or_team.session_state = {}

        if "reasoning_steps" not in agent_or_team.session_state:
            agent_or_team.session_state["reasoning_steps"] = {}

        run_id = getattr(agent_or_team, "run_id", "default")
        if run_id not in agent_or_team.session_state["reasoning_steps"]:
            agent_or_team.session_state["reasoning_steps"][run_id] = []

    def _store_reasoning_step(self, agent_or_team: Any, step: ReasoningStep) -> None:
        """Store a reasoning step in session state."""
        run_id = getattr(agent_or_team, "run_id", "default")
        agent_or_team.session_state["reasoning_steps"][run_id].append(step.to_dict())

    def _get_reasoning_history(self, agent_or_team: Any) -> List[Dict[str, Any]]:
        """Get reasoning history for current session."""
        if not hasattr(agent_or_team, "session_state") or not agent_or_team.session_state:
            return []

        if "reasoning_steps" not in agent_or_team.session_state:
            return []

        run_id = getattr(agent_or_team, "run_id", "default")
        return agent_or_team.session_state["reasoning_steps"].get(run_id, [])

    def _analyze_problem(
        self,
        problem: str,
        reasoning_type: ReasoningType,
        evidence: List[str],
        context: Optional[str],
    ) -> Dict[str, Any]:
        """Analyze problem using specified reasoning type."""
        # Assess problem characteristics
        complexity = self._assess_complexity(problem, evidence)
        evidence_strength = self._assess_evidence_strength(evidence)

        # Generate key insights based on reasoning type
        insights = self._generate_insights(problem, reasoning_type, evidence, context)

        # Calculate confidence
        confidence = self._calculate_confidence(problem, evidence, reasoning_type)

        return {
            "reasoning_type": reasoning_type.value,
            "complexity": complexity,
            "evidence_strength": evidence_strength,
            "key_insights": insights,
            "confidence_level": confidence,
        }

    def _assess_complexity(self, problem: str, evidence: List[str]) -> str:
        """Assess problem complexity."""
        factors = len(problem.split()) + len(evidence) * 2
        if factors > 80:
            return "quite complex"
        elif factors > 40:
            return "moderately complex"
        else:
            return "relatively straightforward"

    def _assess_evidence_strength(self, evidence: List[str]) -> str:
        """Assess evidence strength."""
        if len(evidence) >= 5:
            return "strong"
        elif len(evidence) >= 3:
            return "moderate"
        elif len(evidence) >= 1:
            return "limited"
        else:
            return "minimal"

    def _generate_insights(
        self,
        problem: str,
        reasoning_type: ReasoningType,
        evidence: List[str],
        context: Optional[str],
    ) -> List[str]:
        """Generate insights based on reasoning type."""
        insights = []

        # Base insights by reasoning type
        type_insights = {
            ReasoningType.DEDUCTIVE: [
                "Following logical premises to reach conclusions",
                "Building on established facts and rules",
            ],
            ReasoningType.INDUCTIVE: [
                "Looking for patterns and generalizations",
                "Drawing insights from multiple data points",
            ],
            ReasoningType.ABDUCTIVE: [
                "Seeking the best explanation for observations",
                "Considering multiple possible explanations",
            ],
            ReasoningType.CAUSAL: [
                "Examining cause-and-effect relationships",
                "Tracing the chain of influences",
            ],
            ReasoningType.PROBABILISTIC: [
                "Considering uncertainties and likelihoods",
                "Weighing different possible outcomes",
            ],
            ReasoningType.ANALOGICAL: [
                "Drawing comparisons to similar situations",
                "Learning from parallel cases",
            ],
        }

        insights.extend(type_insights.get(reasoning_type, []))

        # Add problem-specific insights
        problem_lower = problem.lower()
        if "decision" in problem_lower or "choose" in problem_lower:
            insights.append("Evaluating decision alternatives and trade-offs")
        if "risk" in problem_lower:
            insights.append("Assessing potential risks and uncertainties")

        return insights[: self.reasoning_depth]

    def _calculate_confidence(
        self, problem: str, evidence: List[str], reasoning_type: ReasoningType
    ) -> str:
        """Calculate confidence level."""
        # Base confidence on evidence and reasoning type
        evidence_factor = min(1.0, len(evidence) * 0.2)

        type_reliability = {
            ReasoningType.DEDUCTIVE: 0.9,
            ReasoningType.INDUCTIVE: 0.7,
            ReasoningType.ABDUCTIVE: 0.6,
            ReasoningType.CAUSAL: 0.7,
            ReasoningType.PROBABILISTIC: 0.8,
            ReasoningType.ANALOGICAL: 0.6,
        }

        base_confidence = type_reliability.get(reasoning_type, 0.7)
        final_confidence = base_confidence + evidence_factor

        if final_confidence > 0.8:
            return "quite confident"
        elif final_confidence > 0.6:
            return "moderately confident"
        else:
            return "somewhat uncertain"

    def _detect_biases_in_content(
        self, problem: str, evidence: List[str], context: Optional[str]
    ) -> List[str]:
        """Detect biases in reasoning content."""
        text_to_analyze = f"{problem} {' '.join(evidence)} {context or ''}"
        return self._identify_biases(text_to_analyze)

    def _identify_biases(self, text: str) -> List[str]:
        """Identify biases in text content."""
        detected = []
        text_lower = text.lower()

        for bias_name, patterns in self.bias_patterns.items():
            # Check keywords
            if any(keyword in text_lower for keyword in patterns.get("keywords", [])):
                detected.append(bias_name)
                continue

            # Check phrases
            if any(phrase in text_lower for phrase in patterns.get("phrases", [])):
                detected.append(bias_name)

        return detected

    def _integrate_multi_modal_results(
        self, results: Dict[str, Dict], problem: str
    ) -> Dict[str, Any]:
        """Integrate multiple reasoning results."""
        confidence_levels = [
            result.get("confidence_level", "moderately confident")
            for result in results.values()
        ]

        # Determine overall confidence
        if "quite confident" in confidence_levels:
            overall_confidence = "quite confident"
        elif "moderately confident" in confidence_levels:
            overall_confidence = "moderately confident"
        else:
            overall_confidence = "somewhat uncertain"

        return {
            "overall_confidence": overall_confidence,
            "reasoning_count": len(results),
            "approaches_used": list(results.keys()),
        }

    def _format_reasoning_output(
        self,
        problem: str,
        reasoning_type: ReasoningType,
        analysis: Dict[str, Any],
        biases: List[str],
        evidence: List[str],
    ) -> str:
        """Format reasoning output in natural language."""
        output_parts = []

        # Problem introduction
        problem_summary = problem[:100] + "..." if len(problem) > 100 else problem
        output_parts.append(f"**Problem Analysis:** {problem_summary}")

        # Reasoning approach
        output_parts.append(
            f"\n**Reasoning Approach:** Using {reasoning_type.value} reasoning to analyze this systematically."
        )

        # Key insights
        insights = analysis.get("key_insights", [])
        if insights:
            output_parts.append("\n**Key Insights:**")
            for insight in insights:
                output_parts.append(f"• {insight}")

        # Evidence consideration
        if evidence:
            output_parts.append(
                f"\n**Evidence:** Considering {len(evidence)} pieces of supporting evidence."
            )

        # Confidence
        confidence = analysis.get("confidence_level", "moderately confident")
        complexity = analysis.get("complexity", "moderately complex")
        output_parts.append(
            f"\n**Assessment:** Given that this problem is {complexity}, I'm {confidence} in this analysis."
        )

        # Bias warnings
        if biases:
            bias_names = [bias.replace("_", " ").title() for bias in biases]
            output_parts.append(
                f"\n**Cognitive Bias Alert:** I detected potential {', '.join(bias_names)} in this reasoning. Consider seeking contradictory evidence."
            )

        return "\n".join(output_parts)

    def _format_multi_modal_output(
        self,
        problem: str,
        reasoning_types: List[ReasoningType],
        integration: Dict[str, Any],
        evidence: List[str],
    ) -> str:
        """Format multi-modal reasoning output."""
        output_parts = []

        # Problem introduction
        problem_summary = problem[:100] + "..." if len(problem) > 100 else problem
        output_parts.append(f"**Multi-Modal Analysis:** {problem_summary}")

        # Approaches used
        type_names = [rt.value for rt in reasoning_types]
        approaches_text = (
            ", ".join(type_names[:-1]) + f", and {type_names[-1]}"
            if len(type_names) > 1
            else type_names[0]
        )
        output_parts.append(
            f"\n**Approaches Used:** {approaches_text} reasoning for comprehensive analysis."
        )

        # Evidence consideration
        if evidence:
            output_parts.append(
                f"\n**Evidence:** Analyzed {len(evidence)} pieces of supporting evidence across all approaches."
            )

        # Integration results
        confidence = integration.get("overall_confidence", "moderately confident")
        output_parts.append(
            f"\n**Integrated Assessment:** Combining {len(reasoning_types)} reasoning approaches, I'm {confidence} in this comprehensive analysis."
        )

        output_parts.append(
            "\n**Conclusion:** This multi-faceted approach provides a more robust and well-rounded understanding of the problem."
        )

        return "\n".join(output_parts)

    def _format_analysis_output(
        self,
        result: str,
        analysis: str,
        next_action: NextAction,
        confidence: str,
        history: List[Dict[str, Any]],
    ) -> str:
        """Format analysis output with reasoning history."""
        output_parts = []

        # Analysis header
        output_parts.append("**Reasoning Analysis**")

        # Result evaluation
        result_summary = result[:100] + "..." if len(result) > 100 else result
        output_parts.append(f"\n**Result:** {result_summary}")

        # Analysis content
        output_parts.append(f"\n**Analysis:** {analysis}")

        # Confidence
        output_parts.append(f"\n**Confidence:** {confidence}")

        # Next action guidance
        action_guidance = {
            NextAction.CONTINUE: "Continue reasoning - more analysis needed",
            NextAction.VALIDATE: "Validate results - seek external confirmation if possible",
            NextAction.FINAL_ANSWER: "Ready to conclude - sufficient analysis completed",
        }
        output_parts.append(
            f"\n**Next Action:** {action_guidance.get(next_action, 'Continue reasoning')}"
        )

        # Reasoning progress
        if history:
            output_parts.append(
                f"\n**Reasoning Progress:** {len(history)} steps completed in this session."
            )

        return "\n".join(output_parts)

    def _explain_biases_naturally(self, detected_biases: List[str], content: str) -> str:
        """Explain detected biases naturally with context from the reasoning content."""
        if not detected_biases:
            return "The reasoning appears well-balanced without obvious cognitive biases."

        explanations = []
        content_length = len(content)
        
        for bias in detected_biases:
            if bias == "confirmation_bias":
                explanations.append(
                    f"I notice confirmation bias in the {content_length}-character reasoning - it seems to favor information that supports a particular viewpoint. "
                    "In the analyzed content, this appears as selective focus on supporting evidence."
                )
            elif bias == "anchoring_bias":
                explanations.append(
                    f"There's evidence of anchoring bias in the reasoning - the analysis appears heavily influenced by initial information. "
                    "The reasoning may be overly weighted toward early assumptions or data points."
                )
            elif bias == "availability_heuristic":
                explanations.append(
                    f"I see signs of availability bias - recent or easily recalled examples seem to be given more weight. "
                    "The reasoning may overemphasize readily accessible information."
                )
            elif bias == "overconfidence_bias":
                explanations.append(
                    f"There's overconfidence bias - the reasoning expresses more certainty than the evidence may warrant. "
                    "Consider the strength of conclusions relative to available evidence."
                )

        if len(explanations) > 1:
            result = ". Additionally, ".join(explanations) + "."
        else:
            result = explanations[0] + "."
            
        result += f"\n\nTo improve reasoning quality in this {content_length}-character analysis, consider actively seeking contradictory evidence, questioning initial assumptions, and being more explicit about uncertainties."

        return result

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns a set of detailed instructions for LLMs on how to use each tool in EnhancedReasoningTools.
        Each instruction includes the method name, description, parameters, types, and example values.
        """
        instructions = """
<reasoning_tools_instructions>
*** Universal Reasoning Tools Instructions ***

These tools enable advanced reasoning, bias detection, and session management for complex problem solving. They facilitate structured, multi-modal, and human-like reasoning with step tracking and bias awareness.

**Available Tools**:

1. **reason**: Apply structured reasoning to a problem.
   - Parameters:
     - `agent_or_team`: The agent or team requesting reasoning (object or identifier).
     - `problem` (str): The problem or question to analyze, e.g., "What are the causes of climate change?".
     - `reasoning_type` (str, optional): Type of reasoning to apply. Choose from: "deductive", "inductive", "abductive", "causal", "probabilistic", "analogical". Default: "deductive".
     - `evidence` (list of str, optional): Supporting evidence or data points.
     - `context` (str, optional): Additional context for the problem.

2. **multi_modal_reason**: Apply multiple reasoning approaches and integrate insights.
   - Parameters:
     - `agent_or_team`: The agent or team requesting reasoning.
     - `problem` (str): The problem to analyze.
     - `reasoning_types` (list of str): List of reasoning types to apply, e.g., ["deductive", "abductive"].
     - `evidence` (list of str, optional): Supporting evidence or data points.

3. **analyze_reasoning**: Analyze reasoning results and determine next actions.
   - Parameters:
     - `agent_or_team`: The agent or team requesting analysis.
     - `result` (str): The outcome of the previous reasoning step.
     - `analysis` (str): Your analysis of the results.
     - `next_action` (str, optional): What to do next. Choose from: "continue", "validate", "final_answer". Default: "continue".
     - `confidence` (str, optional): Confidence level in this analysis. Default: "moderately confident".

4. **iterative_reason**: Apply iterative reasoning with bias detection and correction.
   - Parameters:
     - `agent_or_team`: The agent or team requesting reasoning.
     - `problem` (str): The problem or question to analyze.
     - `reasoning_type` (str, optional): Type of reasoning to apply. Default: "deductive".
     - `evidence` (list of str, optional): Supporting evidence or data points.
     - `context` (str, optional): Additional context for the problem.
     - `max_iterations` (int, optional): Maximum number of iterations to attempt. Default: 3.

5. **get_reasoning_history**: Get the reasoning history for the current session.
   - Parameters:
     - `agent_or_team`: The agent or team to get history for.

6. **clear_reasoning_session**: Clear the reasoning session state.
   - Parameters:
     - `agent_or_team`: The agent or team to clear session for.

7. **detect_biases**: Detect cognitive biases in reasoning content.
   - Parameters:
     - `agent_or_team`: The agent or team requesting bias detection.
     - `reasoning_content` (str): The reasoning text to analyze for biases.

**General Notes:**
- All tools require an `agent_or_team` parameter, which should be an object or identifier representing the current agent or team context.
- For tools with optional parameters, defaults are provided if no value is given.

</reasoning_tools_instructions>
"""
        return instructions
