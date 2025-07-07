from fastapi.testclient import TestClient
from backend.api import app
from backend.mcp_controller import TaskSpec, ErrorPolicy, planner, engine
from eudaimonia.core import storage

client = TestClient(app)


def test_suggest_empty(monkeypatch):
    monkeypatch.setattr(planner, "tasks", [])
    res = client.post("/tasks/suggest", json={"goal": "foo"})
    assert res.status_code == 200
    assert res.json() == []


def test_execute_flow(tmp_path, monkeypatch):
    task = TaskSpec(
        id="t1",
        label="demo",
        description="demo task",
        params_schema={
            "type": "object",
            "properties": {"x": {"type": "number"}},
            "required": ["x"],
        },
        schedule="now",
        risk="low",
        idempotent=True,
    )
    monkeypatch.setattr(engine, "executed", set())
    storage._db_cache = {}
    res = client.post(
        "/tasks/execute",
        json={
            "task": task.dict(),
            "params": {"x": 1},
            "policy": ErrorPolicy(retry=0).dict(),
            "context": {},
        },
    )
    assert res.status_code == 200
    assert res.json()["status"] == "success"
