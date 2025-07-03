import os
from datetime import datetime
from pathlib import Path
from tinydb import TinyDB, Query

DEFAULT_PATH = Path(__file__).resolve().parent / "memory.json"
_db_cache = {}


def _get_db(path=DEFAULT_PATH):
    path = str(path)
    if path not in _db_cache:
        _db_cache[path] = TinyDB(path)
    return _db_cache[path]


def append_event(event_type: str, data: dict, *, path: str = DEFAULT_PATH) -> None:
    """Append an event dict to the TinyDB store."""
    db = _get_db(path)
    db.insert({"type": event_type, "data": data, "ts": datetime.utcnow().isoformat()})


def get_recent_events(event_type: str, limit: int = 10, *, path: str = DEFAULT_PATH) -> list:
    """Return up to ``limit`` most recent events of ``event_type``."""
    db = _get_db(path)
    q = Query()
    events = db.search(q.type == event_type)
    events.sort(key=lambda e: e.get("ts", ""), reverse=True)
    return events[:limit]


def clear_store(*, path: str = DEFAULT_PATH) -> None:
    """Utility to clear all events in the store (mainly for tests)."""
    db = _get_db(path)
    db.truncate()
