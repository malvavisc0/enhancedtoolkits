"""Orchestration and planning toolkit.

This module provides a small, schema-friendly way for an agent (LLM) to keep an
explicit plan, manage task dependencies, and track progress.

Design goals:
- Deterministic, auditable state transitions (no hidden LLM logic).
- JSON-string outputs (tool-call friendly).
- Store plan state on the provided `agent_or_team` object (similar to other
  toolkits' session state patterns).

Notes on "load once":
- A process-wide singleton is provided via `get_orchestration_tools()`.
- [`StrictToolkit`](src/enhancedtoolkits/base.py:10) can auto-inject orchestration
  functions into any toolkit instance, so the planning tools are available when
  using any toolkit.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional

from agno.utils.log import log_debug, log_error

from .base import StrictToolkit

TaskStatus = Literal[
    "todo",
    "in_progress",
    "done",
    "blocked",
    "failed",
    "skipped",
]


@dataclass
class PlanTask:  # pylint: disable=too-many-instance-attributes
    """A single task inside a plan."""

    task_id: int
    title: str
    description: Optional[str] = None
    priority: int = 0
    depends_on: List[int] = field(default_factory=list)
    status: TaskStatus = "todo"
    result_summary: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class PlanState:  # pylint: disable=too-many-instance-attributes
    """Plan container stored on the session state."""

    plan_id: str
    goal: str
    constraints: Optional[str] = None
    tasks: Dict[int, PlanTask] = field(default_factory=dict)
    next_task_id: int = 1
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class OrchestrationTools(StrictToolkit):
    """Orchestration + planning toolkit.

    This toolkit is intentionally conservative:
    - It does not generate plans; it stores and manages plans provided by the caller.
    - It provides dependency-aware scheduling primitives.

    All public functions return JSON strings.
    """

    _disable_auto_orchestrator: bool = True

    def __init__(
        self,
        name: str = "enhanced_orchestration_tools",
        add_instructions: bool = True,
        **kwargs: Any,
    ):
        instructions = """
<orchestration_tools>
Plan orchestration: maintain a task graph (dependencies), pick next actions, and track progress.

OUTPUT
- All functions return JSON strings.

TASK STATUS
- todo | in_progress | done | blocked | failed | skipped

BEST PRACTICES
- Keep tasks small and verifiable.
- Use dependencies (depends_on) instead of implicit ordering.
- Call next_actions() to pick executable tasks.

</orchestration_tools>
"""

        super().__init__(
            name=name,
            instructions=instructions if add_instructions else "",
            add_instructions=add_instructions,
            **kwargs,
        )

        # Core API
        self.register(self.create_plan)
        self.register(self.add_task)
        self.register(self.update_task_status)
        self.register(self.next_actions)
        self.register(self.summarize_progress)
        self.register(self.reset_plan)

    # -----------------------------
    # Session state helpers
    # -----------------------------

    @staticmethod
    def _get_session_state(agent_or_team: Any) -> Dict[str, Any]:
        """Return the session state container (attach if missing)."""
        # pylint: disable=protected-access
        
        # DIAGNOSTIC: Log what type we received
        log_debug(f"_get_session_state received type: {type(agent_or_team)}")
        log_debug(f"_get_session_state received value: {agent_or_team}")
     
        if not hasattr(agent_or_team, "_orchestration_session_state"):
            agent_or_team._orchestration_session_state = {}
        return agent_or_team._orchestration_session_state

    def _get_plan(self, agent_or_team: Any) -> Optional[PlanState]:
        state = self._get_session_state(agent_or_team)
        return state.get("plan")

    def _set_plan(self, agent_or_team: Any, plan: Optional[PlanState]) -> None:
        state = self._get_session_state(agent_or_team)
        state["plan"] = plan

    @staticmethod
    def _now() -> float:
        return time.time()

    @staticmethod
    def _format_json(data: Any) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)

    @staticmethod
    def _plan_to_dict(plan: PlanState) -> Dict[str, Any]:
        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "constraints": plan.constraints,
            "created_at": plan.created_at,
            "updated_at": plan.updated_at,
            "tasks": [asdict(t) for _, t in sorted(plan.tasks.items())],
        }

    # -----------------------------
    # Public tool functions
    # -----------------------------

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    def create_plan(
        self,
        agent_or_team: Any,
        goal: str,
        tasks: Optional[List[Dict[str, Any]]] = None,
        constraints: Optional[str] = None,
        max_tasks: int = 50,
    ) -> str:
        """Create (or overwrite) a plan.

        Args:
            agent_or_team: Any object used as a state container (agent/team).
            goal: High-level objective.
            tasks: Optional list of task objects with fields:
                - title (required)
                - description (optional)
                - priority (optional, int)
                - depends_on (optional, list[int])
            constraints: Optional constraints text (budgets, deadlines, etc.).
            max_tasks: Safety limit to avoid enormous plans.

        Returns:
            JSON string with the created plan.
        """
        try:
            if not goal or not goal.strip():
                return self._format_json(
                    {
                        "operation": "create_plan",
                        "ok": False,
                        "error": "goal must be a non-empty string",
                    }
                )

            max_tasks = max(1, min(500, int(max_tasks)))

            plan = PlanState(
                plan_id=str(int(self._now() * 1000)),
                goal=goal.strip(),
                constraints=constraints.strip() if constraints else None,
            )

            incoming = tasks or []
            if len(incoming) > max_tasks:
                incoming = incoming[:max_tasks]

            for item in incoming:
                title = str(item.get("title", "")).strip()
                if not title:
                    continue

                description = item.get("description")
                if description is not None:
                    description = str(description)

                priority_raw = item.get("priority", 0)
                try:
                    priority = int(priority_raw)
                except Exception:  # pylint: disable=broad-exception-caught
                    priority = 0

                depends_on = item.get("depends_on") or []
                if not isinstance(depends_on, list):
                    depends_on = []
                depends_on_ids: List[int] = []
                for dep in depends_on:
                    try:
                        depends_on_ids.append(int(dep))
                    except Exception:  # pylint: disable=broad-exception-caught
                        continue

                task_id = plan.next_task_id
                plan.next_task_id += 1
                plan.tasks[task_id] = PlanTask(
                    task_id=task_id,
                    title=title,
                    description=description,
                    priority=priority,
                    depends_on=depends_on_ids,
                )

            plan.updated_at = self._now()
            self._set_plan(agent_or_team, plan)

            return self._format_json(
                {
                    "operation": "create_plan",
                    "ok": True,
                    "plan": self._plan_to_dict(plan),
                }
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"create_plan failed: {exc}")
            return self._format_json(
                {
                    "operation": "create_plan",
                    "ok": False,
                    "error": str(exc),
                }
            )

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def add_task(
        self,
        agent_or_team: Any,
        title: str,
        description: Optional[str] = None,
        priority: int = 0,
        depends_on: Optional[List[int]] = None,
    ) -> str:
        """Add a task to the current plan."""
        try:
            plan = self._get_plan(agent_or_team)
            if plan is None:
                return self._format_json(
                    {
                        "operation": "add_task",
                        "ok": False,
                        "error": "no active plan (call create_plan first)",
                    }
                )

            title = (title or "").strip()
            if not title:
                return self._format_json(
                    {
                        "operation": "add_task",
                        "ok": False,
                        "error": "title must be a non-empty string",
                    }
                )

            dep_ids: List[int] = []
            for dep in depends_on or []:
                try:
                    dep_ids.append(int(dep))
                except Exception:  # pylint: disable=broad-exception-caught
                    continue

            task_id = plan.next_task_id
            plan.next_task_id += 1
            plan.tasks[task_id] = PlanTask(
                task_id=task_id,
                title=title,
                description=description,
                priority=int(priority),
                depends_on=dep_ids,
            )
            plan.updated_at = self._now()

            return self._format_json(
                {
                    "operation": "add_task",
                    "ok": True,
                    "task": asdict(plan.tasks[task_id]),
                    "plan_id": plan.plan_id,
                }
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"add_task failed: {exc}")
            return self._format_json(
                {"operation": "add_task", "ok": False, "error": str(exc)}
            )

    def update_task_status(
        self,
        agent_or_team: Any,
        task_id: int,
        status: TaskStatus,
        result_summary: Optional[str] = None,
    ) -> str:
        """Update the status of a task."""
        try:
            plan = self._get_plan(agent_or_team)
            if plan is None:
                return self._format_json(
                    {
                        "operation": "update_task_status",
                        "ok": False,
                        "error": "no active plan (call create_plan first)",
                    }
                )

            task_id_int = int(task_id)
            task = plan.tasks.get(task_id_int)
            if task is None:
                return self._format_json(
                    {
                        "operation": "update_task_status",
                        "ok": False,
                        "error": f"task_id {task_id_int} not found",
                    }
                )

            task.status = status
            task.result_summary = result_summary
            task.updated_at = self._now()
            plan.updated_at = self._now()

            return self._format_json(
                {
                    "operation": "update_task_status",
                    "ok": True,
                    "task": asdict(task),
                    "plan_id": plan.plan_id,
                }
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"update_task_status failed: {exc}")
            return self._format_json(
                {
                    "operation": "update_task_status",
                    "ok": False,
                    "error": str(exc),
                }
            )

    def next_actions(
        self,
        agent_or_team: Any,
        max_actions: int = 1,
        mark_in_progress: bool = True,
    ) -> str:
        """Return executable tasks (deps satisfied), optionally marking them in-progress."""
        try:
            plan = self._get_plan(agent_or_team)
            if plan is None:
                return self._format_json(
                    {
                        "operation": "next_actions",
                        "ok": False,
                        "error": "no active plan (call create_plan first)",
                    }
                )

            max_actions = max(1, min(50, int(max_actions)))

            def deps_satisfied(task: PlanTask) -> bool:
                for dep_id in task.depends_on:
                    dep = plan.tasks.get(dep_id)
                    if dep is None:
                        # Unknown dependency -> treat as unsatisfied
                        return False
                    if dep.status != "done":
                        return False
                return True

            ready = [
                t
                for t in plan.tasks.values()
                if t.status == "todo" and deps_satisfied(t)
            ]

            ready.sort(key=lambda t: (-t.priority, t.task_id))
            selected = ready[:max_actions]

            if mark_in_progress:
                for t in selected:
                    t.status = "in_progress"
                    t.updated_at = self._now()
                plan.updated_at = self._now()

            return self._format_json(
                {
                    "operation": "next_actions",
                    "ok": True,
                    "plan_id": plan.plan_id,
                    "actions": [asdict(t) for t in selected],
                }
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"next_actions failed: {exc}")
            return self._format_json(
                {"operation": "next_actions", "ok": False, "error": str(exc)}
            )

    def summarize_progress(self, agent_or_team: Any) -> str:
        """Summarize plan progress."""
        try:
            plan = self._get_plan(agent_or_team)
            if plan is None:
                return self._format_json(
                    {
                        "operation": "summarize_progress",
                        "ok": False,
                        "error": "no active plan (call create_plan first)",
                    }
                )

            counts: Dict[str, int] = {
                "todo": 0,
                "in_progress": 0,
                "done": 0,
                "blocked": 0,
                "failed": 0,
                "skipped": 0,
            }

            for t in plan.tasks.values():
                counts[t.status] = counts.get(t.status, 0) + 1

            total = len(plan.tasks)
            done = counts.get("done", 0)
            completion_ratio = (done / total) if total else 0.0

            # Identify blocked/failed tasks with short summaries
            problematic = [
                asdict(t)
                for t in plan.tasks.values()
                if t.status in ("blocked", "failed")
            ]

            log_debug(f"Orchestration summary: {total} total, {done} done")

            return self._format_json(
                {
                    "operation": "summarize_progress",
                    "ok": True,
                    "plan_id": plan.plan_id,
                    "goal": plan.goal,
                    "counts": counts,
                    "completion_ratio": round(completion_ratio, 4),
                    "problematic_tasks": problematic,
                }
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"summarize_progress failed: {exc}")
            return self._format_json(
                {
                    "operation": "summarize_progress",
                    "ok": False,
                    "error": str(exc),
                }
            )

    def reset_plan(self, agent_or_team: Any) -> str:
        """Clear the current plan."""
        try:
            self._set_plan(agent_or_team, None)
            return self._format_json(
                {"operation": "reset_plan", "ok": True, "result": "cleared"}
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"reset_plan failed: {exc}")
            return self._format_json(
                {"operation": "reset_plan", "ok": False, "error": str(exc)}
            )


_ORCHESTRATION_SINGLETON: Optional[OrchestrationTools] = None


def get_orchestration_tools() -> OrchestrationTools:
    """Return a process-wide singleton instance of `OrchestrationTools`."""
    global _ORCHESTRATION_SINGLETON  # pylint: disable=global-statement
    if _ORCHESTRATION_SINGLETON is None:
        _ORCHESTRATION_SINGLETON = OrchestrationTools(add_instructions=False)
    return _ORCHESTRATION_SINGLETON
