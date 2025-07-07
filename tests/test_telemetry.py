from backend.telemetry.metrics import get_stats
from backend.telemetry.telemetry import traced_llm_call
import asyncio


def test_get_stats_returns_dict(monkeypatch):
    class FakeLangfuse:
        def get_stats(self, start=None, end=None):
            return {"calls": 1}

    monkeypatch.setattr('backend.telemetry.metrics.Langfuse', FakeLangfuse)
    assert get_stats() == {"calls": 1}


def test_traced_llm_call_decorator(monkeypatch):
    called = {}

    async def dummy(x):
        called['x'] = x
        return x * 2

    class FakeLF:
        def trace_start(self, name):
            pass

        def trace_success(self, res):
            called['traced'] = True

        def trace_error(self, err):
            pass

    monkeypatch.setattr('backend.telemetry.telemetry.Langfuse', lambda: FakeLF())

    wrapped = traced_llm_call('dummy')(dummy)
    res = asyncio.run(wrapped(3))
    assert res == 6
    assert called['x'] == 3
    assert called.get('traced') is True
