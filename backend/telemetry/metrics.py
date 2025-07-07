from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

try:
    from langfuse import Langfuse
except Exception:
    Langfuse = None  # type: ignore


def get_stats(hours: int = 24) -> dict[str, Any]:
    """Aggregate Langfuse stats over the given period.

    Returns an empty dict if Langfuse is unavailable or an error occurs.
    """
    if not Langfuse:
        return {}

    try:
        lf = Langfuse()
        end = datetime.utcnow()
        start = end - timedelta(hours=hours)
        return lf.get_stats(start=start, end=end)
    except Exception:
        return {}
