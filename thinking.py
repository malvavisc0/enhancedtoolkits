"""
Enhanced Thinking Tools

An advanced thinking tool that builds on Agno's ThinkingTools pattern while adding:
- Structured thinking types and frameworks
- Cognitive bias detection and mitigation
- Context-aware thought organization
- Natural language output with reasoning depth
- Quality assessment and improvement suggestions

Author: malvavisc0
License: MIT
Version: 1.0.0
"""

import hashlib
import random
from datetime import datetime
from enum import Enum
from textwrap import dedent
from typing import Any, Dict, List, Optional

from agno.tools import Toolkit
from agno.utils.log import log_debug, logger


class ThinkingType(Enum):
    """Types of structured thinking approaches."""

    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    EVALUATION = "evaluation"
    REFLECTION = "reflection"
    PLANNING = "planning"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE = "creative"
    CRITICAL = "critical"


class CognitiveBias(Enum):
    """Common cognitive biases to detect in thinking."""

    CONFIRMATION_BIAS = "confirmation_bias"
    ANCHORING_BIAS = "anchoring_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"
    OVERCONFIDENCE_BIAS = "overconfidence_bias"
    HINDSIGHT_BIAS = "hindsight_bias"
    FRAMING_EFFECT = "framing_effect"


class EnhancedThinkingTools(Toolkit):
    """
    Enhanced Thinking Tools

    Builds on Agno's ThinkingTools pattern while adding sophisticated cognitive capabilities:
    - Structured thinking types for different cognitive approaches
    - Cognitive bias detection and awareness
    - Context integration with problems and evidence
    - Quality assessment and improvement suggestions
    - Natural language output without technical metrics
    """

    def __init__(
        self,
        think: bool = True,
        enable_bias_detection: bool = True,
        enable_quality_assessment: bool = True,
        thinking_depth: int = 3,
        instructions: Optional[str] = None,
        add_instructions: bool = False,
        **kwargs,
    ):
        # Enhanced instructions that build on Agno pattern
        if instructions is None:
            self.instructions = dedent(
                """\
                ## Using the Enhanced Thinking Tool

                The Enhanced Thinking Tool is your advanced cognitive scratchpad for developing, organizing, and improving your thought process before taking action or responding to the user. It produces natural language output with reasoning depth, cognitive insights, and actionable suggestions.

                ### What this tool enables you to do

                - Apply structured thinking approaches: analysis, synthesis, evaluation, reflection, planning, problem solving, creative, and critical thinking
                - Integrate specific context and available evidence into your thoughts
                - Detect and report potential cognitive biases, helping you actively mitigate them
                - Build logical chains of reasoning toward problem resolution
                - Reflect on the quality, clarity, and depth of your thinking process
                - Receive feedback and suggestions to improve your thought quality with each step

                ### Best Practices

                - Select the most appropriate thinking type for your current cognitive task
                - Explicitly connect your thoughts to the specific problem, context, and supporting evidence
                - Express your confidence level in natural language (e.g., "quite confident", "uncertain")—avoid numeric confidence scores
                - Remain vigilant for cognitive biases; the tool will also highlight any it detects in your reasoning
                - Use the tool iteratively to develop, refine, and deepen your insights
                - When using another tool (such as a search, data, or external API tool), incorporate its results into your thinking and final answer if they add value or relevant context
                - Reflect on your thinking process and seek opportunities for improvement

                ### Example Usage

                - Break down a complex problem before proposing a solution
                - Synthesize information from multiple sources and evidence
                - Evaluate the strengths and weaknesses of different approaches
                - Plan next steps or strategies based on your analysis
                - Reflect on your reasoning to identify gaps or biases
                """
            )
        else:
            self.instructions = instructions

        # Configuration
        self.enable_bias_detection = enable_bias_detection
        self.enable_quality_assessment = enable_quality_assessment
        self.thinking_depth = max(1, min(10, thinking_depth))

        # Bias detection patterns
        self.bias_patterns = self._initialize_bias_patterns()

        # Register tools
        tools = []
        if think:
            tools.append(self.iterative_think)
            tools.append(self.think)

        super().__init__(
            name="enhanced_thinking_tools",
            instructions=self.instructions,
            add_instructions=add_instructions,
            tools=tools,
            **kwargs,
        )

    def iterative_think(
        self,
        agent: Any,
        thought: str,
        thinking_type: ThinkingType = ThinkingType.ANALYSIS,
        context: Optional[str] = None,
        evidence: Optional[List[str]] = None,
        confidence: Optional[str] = None,
        max_iterations: int = 3,
    ) -> str:
        """
        Iteratively applies thinking, bias detection, and quality assessment, refining the thought until no major bias or low quality is detected or the iteration limit is reached.

        Args:
            agent: The agent or team doing the thinking
            thought: The initial thought content to process
            thinking_type: Type of thinking approach being used
            context: Additional context for the thought
            evidence: Supporting evidence or data points
            confidence: Natural language confidence expression
            max_iterations: Maximum number of iterations

        Returns:
            Natural language summary of the iterative thinking process and final thought
        """
        major_biases = {
            "confirmation_bias",
            "anchoring_bias",
            "overconfidence_bias",
            "availability_heuristic",
            "hindsight_bias",
            "framing_effect",
        }
        min_quality = 0.6  # Minimum acceptable overall quality score
        history = []
        current_thought = thought
        current_thinking_type = thinking_type
        current_context = context
        current_evidence = evidence
        current_confidence = confidence
        iteration = 0
        last_biases = []
        last_quality = 1.0

        while iteration < max_iterations:
            # Step 1: Generate enhanced thought
            output = self.think(
                agent,
                current_thought,
                current_thinking_type,
                current_context,
                current_evidence,
                current_confidence,
            )
            # Retrieve last enhanced thought from session state
            enhanced_thought = agent.session_state["enhanced_thoughts"][-1]
            detected_biases = enhanced_thought.get("detected_biases", [])
            quality_assessment = enhanced_thought.get("quality_assessment", {})
            overall_quality = quality_assessment.get("overall_score", 1.0)
            history.append(
                {
                    "iteration": iteration + 1,
                    "output": output,
                    "biases": detected_biases,
                    "quality": overall_quality,
                }
            )
            # Step 2: Check for major bias or low quality
            major_found = [b for b in detected_biases if b in major_biases]
            if not major_found and overall_quality >= min_quality:
                break
            # Step 3: Reframe thought to address bias/quality
            bias_names = [b.replace("_", " ").title() for b in major_found]
            bias_text = ", ".join(bias_names) if bias_names else ""
            quality_text = ""
            if overall_quality < min_quality:
                quality_text = (
                    f"Previous thought had low quality score ({overall_quality:.2f})."
                )
            prompt = (
                f"Previous thought:\n{current_thought}\n\n"
                f"{'Bias detected: ' + bias_text + '.' if bias_text else ''} "
                f"{quality_text} "
                f"Revise your thought by explicitly addressing these issues. "
                f"Add counterarguments, alternative perspectives, clarify reasoning, or express more uncertainty as needed. "
                f"Narrate what you changed and why."
            )
            current_thought = prompt
            last_biases = major_found
            last_quality = overall_quality
            iteration += 1

        # Compose output
        output_parts = []
        for step in history:
            output_parts.append(
                f"**Iteration {step['iteration']} Thinking:**\n{step['output']}"
            )
            if step["biases"]:
                bias_names = [b.replace("_", " ").title() for b in step["biases"]]
                output_parts.append(f"\nBiases detected: {', '.join(bias_names)}")
            else:
                output_parts.append("\nNo major bias detected.")
            if step["quality"] < min_quality:
                output_parts.append(f"\nQuality below threshold: {step['quality']:.2f}")
            else:
                output_parts.append(f"\nQuality: {step['quality']:.2f}")

        if (last_biases or last_quality < min_quality) and iteration == max_iterations:
            output_parts.append(
                "\nMaximum iterations reached. Some bias or quality issues may remain, and further review is recommended."
            )
        else:
            output_parts.append(
                "\nFinal thought is considered balanced and high-quality."
            )

        return "\n\n".join(output_parts)

    def _initialize_bias_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize cognitive bias detection patterns."""
        return {
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
                "phrases": [
                    "I'm 100% sure",
                    "there's no doubt",
                    "absolutely certain",
                    "definitely will",
                ],
            },
            "hindsight_bias": {
                "keywords": [
                    "obvious",
                    "predictable",
                    "should have known",
                    "saw it coming",
                ],
                "phrases": ["it was obvious", "should have seen", "predictable outcome"],
            },
            "framing_effect": {
                "keywords": ["depends on", "way you look", "perspective", "frame"],
                "phrases": ["depends how you frame", "way of looking", "from this angle"],
            },
        }

    def think(
        self,
        agent: Any,
        thought: str,
        thinking_type: ThinkingType = ThinkingType.ANALYSIS,
        context: Optional[str] = None,
        evidence: Optional[List[str]] = None,
        confidence: Optional[str] = None,
    ) -> str:
        """
        Enhanced thinking tool with structured reasoning and cognitive awareness.

        Args:
            agent: The agent or team doing the thinking
            thought: The thought content to process and store
            thinking_type: Type of thinking approach being used
            context: Additional context for the thought (problem, situation, etc.)
            evidence: Supporting evidence or data points
            confidence: Natural language confidence expression (e.g., "quite confident", "uncertain")

        Returns:
            Natural language summary of thinking progress with cognitive insights
        """
        try:
            log_debug(f"Enhanced Thought ({thinking_type.value}): {thought}")

            # Initialize session state if needed
            if agent.session_state is None:
                agent.session_state = {}
            if "enhanced_thoughts" not in agent.session_state:
                agent.session_state["enhanced_thoughts"] = []
            if "thinking_patterns" not in agent.session_state:
                agent.session_state["thinking_patterns"] = {
                    "type_counts": {},
                    "bias_detections": [],
                    "quality_scores": [],
                    "contexts": [],
                }

            # Generate unique thought ID
            thought_id = self._generate_thought_id()

            # Analyze thought for cognitive biases
            detected_biases = []
            if self.enable_bias_detection:
                detected_biases = self._detect_biases_in_thought(thought)

            # Assess thought quality
            quality_assessment = {}
            if self.enable_quality_assessment:
                quality_assessment = self._assess_thought_quality(
                    thought, thinking_type, context, evidence
                )

            # Create enhanced thought record
            enhanced_thought = {
                "id": thought_id,
                "content": thought,
                "type": thinking_type.value,
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "evidence": evidence or [],
                "confidence": confidence,
                "detected_biases": [bias.value for bias in detected_biases],
                "quality_assessment": quality_assessment,
                "connections": [],  # For future use in reasoning chains
            }

            # Store the enhanced thought
            agent.session_state["enhanced_thoughts"].append(enhanced_thought)

            # Update thinking patterns
            self._update_thinking_patterns(agent, enhanced_thought)

            # Generate natural language output
            output = self._format_thinking_output(
                enhanced_thought,
                agent.session_state["enhanced_thoughts"],
                detected_biases,
                quality_assessment,
            )

            return output

        except Exception as e:
            logger.error(f"Error in enhanced thinking: {e}")
            return f"I encountered an issue while processing this thought: {e}. Let me try a different approach."

    def _generate_thought_id(self) -> str:
        """Generate unique thought ID."""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(
            f"{timestamp}_{random.randint(1000, 9999)}".encode()
        ).hexdigest()[:8]

    def _detect_biases_in_thought(self, thought: str) -> List[CognitiveBias]:
        """Detect cognitive biases in thought content."""
        detected_biases = []
        thought_lower = thought.lower()

        for bias_name, patterns in self.bias_patterns.items():
            # Check keywords
            if any(keyword in thought_lower for keyword in patterns.get("keywords", [])):
                try:
                    detected_biases.append(CognitiveBias(bias_name))
                except ValueError:
                    continue

            # Check phrases
            if any(phrase in thought_lower for phrase in patterns.get("phrases", [])):
                try:
                    detected_biases.append(CognitiveBias(bias_name))
                except ValueError:
                    continue

        return list(set(detected_biases))  # Remove duplicates

    def _assess_thought_quality(
        self,
        thought: str,
        thinking_type: ThinkingType,
        context: Optional[str],
        evidence: Optional[List[str]],
    ) -> Dict[str, Any]:
        """Assess the quality of a thought."""
        assessment = {
            "depth": self._assess_thinking_depth(thought),
            "clarity": self._assess_thinking_clarity(thought),
            "evidence_integration": self._assess_evidence_integration(thought, evidence),
            "context_relevance": self._assess_context_relevance(thought, context),
            "type_appropriateness": self._assess_type_appropriateness(
                thought, thinking_type
            ),
        }

        # Calculate overall quality (for internal use, not shown to user)
        overall_score = sum(assessment.values()) / len(assessment)
        assessment["overall_score"] = overall_score

        return assessment

    def _assess_thinking_depth(self, thought: str) -> float:
        """Assess the depth of thinking."""
        # Simple heuristics for thinking depth
        word_count = len(thought.split())
        question_count = thought.count("?")
        reasoning_words = sum(
            1
            for word in ["because", "therefore", "however", "although", "since"]
            if word in thought.lower()
        )

        depth_score = min(
            1.0, (word_count / 50) + (question_count * 0.1) + (reasoning_words * 0.1)
        )
        return depth_score

    def _assess_thinking_clarity(self, thought: str) -> float:
        """Assess the clarity of thinking."""
        # Simple clarity assessment
        sentence_count = max(
            1, thought.count(".") + thought.count("!") + thought.count("?")
        )
        avg_sentence_length = len(thought.split()) / sentence_count

        # Optimal sentence length is around 15-20 words
        clarity_score = max(0.0, 1.0 - abs(avg_sentence_length - 17.5) / 17.5)
        return min(1.0, clarity_score)

    def _assess_evidence_integration(
        self, thought: str, evidence: Optional[List[str]]
    ) -> float:
        """Assess how well the thought integrates evidence."""
        if not evidence:
            return 0.5  # Neutral score when no evidence provided

        evidence_mentions = 0
        thought_lower = thought.lower()

        for evidence_item in evidence:
            # Check if evidence concepts are mentioned in thought
            evidence_words = evidence_item.lower().split()[:3]  # First 3 words
            if any(word in thought_lower for word in evidence_words):
                evidence_mentions += 1

        integration_score = min(1.0, evidence_mentions / len(evidence))
        return integration_score

    def _assess_context_relevance(self, thought: str, context: Optional[str]) -> float:
        """Assess how relevant the thought is to the context."""
        if not context:
            return 0.5  # Neutral score when no context provided

        thought_words = set(thought.lower().split())
        context_words = set(context.lower().split())

        # Calculate word overlap
        overlap = len(thought_words.intersection(context_words))
        relevance_score = min(1.0, overlap / max(1, len(context_words)))

        return relevance_score

    def _assess_type_appropriateness(
        self, thought: str, thinking_type: ThinkingType
    ) -> float:
        """Assess how appropriate the thinking type is for the thought content."""
        thought_lower = thought.lower()

        type_indicators = {
            ThinkingType.ANALYSIS: [
                "analyze",
                "break down",
                "examine",
                "components",
                "factors",
            ],
            ThinkingType.SYNTHESIS: [
                "combine",
                "integrate",
                "connect",
                "overall",
                "together",
            ],
            ThinkingType.EVALUATION: [
                "assess",
                "judge",
                "compare",
                "better",
                "worse",
                "evaluate",
            ],
            ThinkingType.REFLECTION: [
                "think about",
                "consider",
                "reflect",
                "meta",
                "approach",
            ],
            ThinkingType.PLANNING: [
                "plan",
                "strategy",
                "steps",
                "next",
                "approach",
                "how to",
            ],
            ThinkingType.PROBLEM_SOLVING: [
                "solve",
                "solution",
                "problem",
                "issue",
                "resolve",
            ],
            ThinkingType.CREATIVE: [
                "creative",
                "innovative",
                "new",
                "different",
                "alternative",
            ],
            ThinkingType.CRITICAL: [
                "critical",
                "question",
                "challenge",
                "assume",
                "verify",
            ],
        }

        indicators = type_indicators.get(thinking_type, [])
        matches = sum(1 for indicator in indicators if indicator in thought_lower)

        appropriateness_score = min(1.0, matches / max(1, len(indicators)))
        return appropriateness_score

    def _update_thinking_patterns(
        self, agent: Any, enhanced_thought: Dict[str, Any]
    ) -> None:
        """Update thinking patterns tracking."""
        patterns = agent.session_state["thinking_patterns"]

        # Update type counts
        thinking_type = enhanced_thought["type"]
        patterns["type_counts"][thinking_type] = (
            patterns["type_counts"].get(thinking_type, 0) + 1
        )

        # Update bias detections
        if enhanced_thought["detected_biases"]:
            patterns["bias_detections"].extend(enhanced_thought["detected_biases"])

        # Update quality scores
        quality_score = enhanced_thought["quality_assessment"].get("overall_score", 0.5)
        patterns["quality_scores"].append(quality_score)

        # Update contexts
        if enhanced_thought["context"]:
            patterns["contexts"].append(enhanced_thought["context"])

    def _format_thinking_output(
        self,
        current_thought: Dict[str, Any],
        all_thoughts: List[Dict[str, Any]],
        detected_biases: List[CognitiveBias],
        quality_assessment: Dict[str, Any],
    ) -> str:
        """Format thinking output in natural, human-like language."""
        output_parts = []

        # Header with thinking type
        thinking_type = current_thought["type"].replace("_", " ").title()
        output_parts.append(f"💭 **{thinking_type} Thinking**")

        # Current thought with context
        if current_thought["context"]:
            output_parts.append(f"\n**Context:** {current_thought['context']}")

        output_parts.append("\n**Current Thought:**")
        output_parts.append(f'"{current_thought["content"]}"')

        # Evidence integration
        if current_thought["evidence"]:
            evidence_count = len(current_thought["evidence"])
            output_parts.append(f"\n**Evidence Considered:** {evidence_count} sources")

        # Confidence expression
        if current_thought["confidence"]:
            output_parts.append(f"\n**Confidence:** {current_thought['confidence']}")

        # Cognitive awareness
        if detected_biases:
            bias_names = [
                bias.value.replace("_", " ").title() for bias in detected_biases
            ]
            if len(bias_names) == 1:
                bias_text = bias_names[0]
            else:
                bias_text = ", ".join(bias_names[:-1]) + f" and {bias_names[-1]}"

            output_parts.append(
                f"\n**Cognitive Awareness:** Detected potential {bias_text} - consider alternative perspectives"
            )
        else:
            output_parts.append(
                "\n**Cognitive Awareness:** Thinking appears balanced and unbiased"
            )

        # Quality insights (natural language)
        quality_insights = self._generate_quality_insights(quality_assessment)
        if quality_insights:
            output_parts.append(f"\n**Thinking Quality:** {quality_insights}")

        # Thinking progress
        total_thoughts = len(all_thoughts)
        if total_thoughts > 1:
            output_parts.append(
                f"\n**Thinking Progress:** {total_thoughts} thoughts developed"
            )

            # Show thinking evolution
            recent_types = [
                t["type"].replace("_", " ").title() for t in all_thoughts[-3:]
            ]
            if len(recent_types) > 1:
                evolution = " → ".join(recent_types)
                output_parts.append(f"**Thinking Evolution:** {evolution}")

        # Next thinking suggestions
        suggestions = self._generate_thinking_suggestions(
            current_thought, all_thoughts, detected_biases
        )
        if suggestions:
            output_parts.append("\n**Next Thinking Suggestions:**")
            for suggestion in suggestions:
                output_parts.append(f"• {suggestion}")

        return "\n".join(output_parts)

    def _generate_quality_insights(self, quality_assessment: Dict[str, Any]) -> str:
        """Generate natural language quality insights."""
        insights = []

        depth = quality_assessment.get("depth", 0.5)
        clarity = quality_assessment.get("clarity", 0.5)
        evidence_integration = quality_assessment.get("evidence_integration", 0.5)

        if depth > 0.7:
            insights.append("Good analytical depth")
        elif depth < 0.3:
            insights.append("Could benefit from deeper analysis")

        if clarity > 0.7:
            insights.append("Clear and well-structured")
        elif clarity < 0.3:
            insights.append("Could be clearer and more focused")

        if evidence_integration > 0.7:
            insights.append("Strong evidence integration")
        elif (
            evidence_integration < 0.3
            and quality_assessment.get("evidence_integration") != 0.5
        ):
            insights.append("Could better integrate available evidence")

        return "; ".join(insights) if insights else "Solid thinking approach"

    def _generate_thinking_suggestions(
        self,
        current_thought: Dict[str, Any],
        all_thoughts: List[Dict[str, Any]],
        detected_biases: List[CognitiveBias],
    ) -> List[str]:
        """Generate suggestions for next thinking steps."""
        suggestions = []

        current_type = current_thought["type"]
        recent_types = [t["type"] for t in all_thoughts[-3:]]

        # Suggest complementary thinking types
        if current_type == "analysis" and "synthesis" not in recent_types:
            suggestions.append("Try synthesis thinking to combine insights")
        elif current_type == "evaluation" and "creative" not in recent_types:
            suggestions.append("Consider creative thinking for alternative approaches")
        elif current_type == "problem_solving" and "critical" not in recent_types:
            suggestions.append("Apply critical thinking to challenge assumptions")

        # Bias-specific suggestions
        if CognitiveBias.CONFIRMATION_BIAS in detected_biases:
            suggestions.append("Actively seek contradictory evidence or viewpoints")
        if CognitiveBias.ANCHORING_BIAS in detected_biases:
            suggestions.append("Consider starting from different initial assumptions")
        if CognitiveBias.OVERCONFIDENCE_BIAS in detected_biases:
            suggestions.append("Explore uncertainties and potential risks")

        # General suggestions based on thinking patterns
        if len(all_thoughts) > 5 and current_type != "reflection":
            suggestions.append("Consider reflection thinking to assess overall progress")

        if not current_thought["evidence"] and current_type != "creative":
            suggestions.append("Gather additional evidence to support reasoning")

        return suggestions[:3]  # Limit to top 3 suggestions
