from __future__ import annotations

import jsonschema
from pydantic import BaseModel
from typing import Any, Dict, List, Literal
import time
from eudaimonia.core import storage


class TaskSpec(BaseModel):
    id: str
    label: str
    description: str
    params_schema: Dict[str, Any]
    schedule: str
    risk: Literal["low", "medium", "high"]
    idempotent: bool


class ErrorPolicy(BaseModel):
    retry: int = 0
    retry_delay: str = "0"
    notify: bool = False
    abort_on_failure: bool = True
    alert_level: str = "info"


class Planner:
    def __init__(self) -> None:
        events = storage.get_recent_events("task_automation", limit=100)
        self.tasks: List[TaskSpec] = [TaskSpec(**e["data"]) for e in events]

    def suggest_tasks(self, goal: str, context: Dict[str, Any]) -> List[TaskSpec]:
        matches = []
        gl = goal.lower()
        for task in self.tasks:
            if gl in task.description.lower() or gl in task.label.lower():
                matches.append(task)
        return matches


class ExecutionEngine:
    def __init__(self) -> None:
        self.executed: set[str] = set()

    def _validate(self, task: TaskSpec, params: Dict[str, Any]) -> None:
        jsonschema.validate(params, task.params_schema)

    def execute(
        self, task: TaskSpec, params: Dict[str, Any], policy: ErrorPolicy
    ) -> Dict[str, Any]:
        if task.idempotent and task.id in self.executed:
            return {"status": "skipped", "reason": "idempotent"}
        self._validate(task, params)
        attempt = 0
        while True:
            try:
                result = {"task": task.id, "params": params, "status": "success"}
                storage.append_event("task_exec", {"task": task.id, "params": params})
                break
            except Exception as exc:  # pragma: no cover - example placeholder
                attempt += 1
                if attempt > policy.retry or policy.abort_on_failure:
                    raise exc
                time.sleep(float(policy.retry_delay))
        self.executed.add(task.id)
        return result


class Dispatcher:
    def __init__(self, engine: ExecutionEngine) -> None:
        self.engine = engine

    def dispatch(
        self,
        task: TaskSpec,
        params: Dict[str, Any],
        policy: ErrorPolicy,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        if task.risk in {"low", "medium"}:
            approved = True
        else:
            approved = context.get("guardian_confirmed", False)
            if not approved:
                raise PermissionError("GuardianMode confirmation required")
        return self.engine.execute(task, params, policy)


planner = Planner()
engine = ExecutionEngine()
dispatcher = Dispatcher(engine)
