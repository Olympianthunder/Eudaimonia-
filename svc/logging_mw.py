import json, time
from datetime import datetime, timezone
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware

LOG = Path("router_metrics.jsonl")

class MetricsLogger(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        t0 = time.time()
        try:
            resp = await call_next(request)
            status = "ok" if 200 <= resp.status_code < 400 else "fail"
        except Exception:
            status = "fail"
            raise
        finally:
            latency_ms = round((time.time() - t0) * 1000)
            rec = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "route": "local_api",
                "path": request.url.path,
                "mode": None,
                "status": status,
                "latency_ms": latency_ms,
                "usd": 0.0
            }
            LOG.write_text(LOG.read_text() + json.dumps(rec) + "\n", encoding="utf-8") if LOG.exists() else LOG.write_text(json.dumps(rec) + "\n", encoding="utf-8")
        return resp
