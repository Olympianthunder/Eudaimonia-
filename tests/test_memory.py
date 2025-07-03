import os
from eudaimonia.core import storage


def test_memory_round_trip(tmp_path):
    db_file = tmp_path / "mem.json"
    storage.append_event("test", {"value": 1}, path=str(db_file))
    events = storage.get_recent_events("test", path=str(db_file))
    assert len(events) == 1
    assert events[0]["data"]["value"] == 1
