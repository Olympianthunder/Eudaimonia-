import json, time
from datetime import datetime, timezone
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware

LOG = Path("router_metrics.jsonl")

class MetricsLogger(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        t0 = time.time()
        status_txt = "ok"
        try:
            resp = await call_next(request)
            if not (200 <= resp.status_code < 400):
                status_txt = "fail"
            return resp
        except Exception:
            status_txt = "fail"
            raise
        finally:
            rec = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "route": "local_api",
                "path": str(request.url.path),
                "status": status_txt,
                "latency_ms": round((time.time() - t0) * 1000),
                "usd": 0.0
            }
            with LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
