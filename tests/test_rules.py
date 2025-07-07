import datetime as dt

from eudaimonia.core import rule_engine


def set_fixed_time(monkeypatch, hour, minute=0):
    class FakeDateTime(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2021, 1, 1, hour, minute, tzinfo=tz)

    monkeypatch.setattr(rule_engine, "datetime", FakeDateTime)


def test_distress_keyword_triggers():
    assert rule_engine.should_trigger_guardian("I need help now", {}) is True


def test_night_watch_trigger(monkeypatch):
    set_fixed_time(monkeypatch, 23, 30)
    assert rule_engine.should_trigger_guardian("just checking", {}) is True


def test_night_watch_non_trigger(monkeypatch):
    set_fixed_time(monkeypatch, 6, 0)
    assert rule_engine.should_trigger_guardian("morning", {}) is False


def test_context_flag_triggers():
    context = {"is_family_context": True}
    assert rule_engine.should_trigger_guardian("", context) is True
