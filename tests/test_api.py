from fastapi.testclient import TestClient

from eudaimonia.api import app, mode_manager
from eudaimonia.core import tts, storage

client = TestClient(app)


def test_speak_endpoint(monkeypatch):
    spoken = {}

    def fake_speak(text: str):
        spoken["text"] = text

    monkeypatch.setattr(tts, "speak", fake_speak)
    res = client.post("/speak", json={"text": "hello"})
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert spoken["text"] == "hello"


def test_mode_endpoint():
    res = client.post("/mode", json={"mode": "default"})
    assert res.status_code == 200
    assert res.json()["active_mode"] == "default"
    assert mode_manager.current_mode.name == "default"


def test_log_endpoint(tmp_path, monkeypatch):
    db_file = tmp_path / "events.json"
    storage._db_cache = {}
    storage.append_event("test", {"value": 42}, path=str(db_file))

    orig = storage.get_recent_events

    def fake_get_recent(event_type: str, limit: int = 10):
        return orig(event_type, limit, path=str(db_file))

    monkeypatch.setattr(storage, "get_recent_events", fake_get_recent)

    res = client.get("/log", params={"type": "test", "limit": 1})
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert data[0]["data"]["value"] == 42
