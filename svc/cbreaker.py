import time
from collections import deque

class CircuitBreaker:
    """
    Sliding-window breaker.
    - Trips when error_rate >= thresh and at least min_events seen.
    - Stays open for open_seconds; during open, .allow() returns False.
    """
    def __init__(self, error_rate_threshold=0.25, window_seconds=60, open_seconds=60, min_events=4):
        self.thresh = float(error_rate_threshold)
        self.window = int(window_seconds)
        self.open_seconds = int(open_seconds)
        self.min_events = int(min_events)
        self.events = deque()  # (timestamp, ok:bool)
        self.open_until = 0.0

    def allow(self) -> bool:
        now = time.time()
        if now < self.open_until:
            return False
        self._gc(now)
        return True

    def record(self, ok: bool):
        now = time.time()
        self.events.append((now, bool(ok)))
        self._gc(now)
        total = len(self.events)
        if total < self.min_events:
            return
        errs = sum(1 for _, okv in self.events if not okv)
        if total and (errs / total) >= self.thresh:
            self.open_until = now + self.open_seconds

    def _gc(self, now: float):
        w = self.window
        while self.events and (now - self.events[0][0]) > w:
            self.events.popleft()
