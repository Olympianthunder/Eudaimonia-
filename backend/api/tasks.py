from fastapi import APIRouter, HTTPException
from typing import Any, Dict

from ..mcp_controller import (
    dispatcher,
    planner,
    TaskSpec,
    ErrorPolicy,
)

router = APIRouter(prefix="/tasks")


@router.post("/suggest")
async def suggest(payload: Dict[str, Any]):
    goal = payload.get("goal", "")
    context = payload.get("context", {})
    tasks = planner.suggest_tasks(goal, context)
    return [t.dict() for t in tasks]


@router.post("/execute")
async def execute(payload: Dict[str, Any]):
    try:
        task = TaskSpec(**payload.get("task", {}))
        params = payload.get("params", {})
        policy = ErrorPolicy(**payload.get("policy", {}))
        context = payload.get("context", {})
    except Exception as exc:  # pragma: no cover - basic validation
        raise HTTPException(status_code=400, detail=str(exc))
    try:
        result = dispatcher.dispatch(task, params, policy, context)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return result
