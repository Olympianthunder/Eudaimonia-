from pathlib import Path
import os, json
import yaml
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# --- router import ---
try:
    from svc.providers.router import call_model
except Exception:
    # last-resort stub
    def call_model(prompt: str, mode: str | None = None):
        return {
            "text": f"[stubbed router] {prompt}",
            "usage": {"usd": 0.0, "model": "stub", "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }

# --- config ---
CFG = {}
cfg_path = Path("config/router.yaml")
if cfg_path.exists():
    CFG = yaml.safe_load(cfg_path.read_text())

BUDGET_DAILY = float(CFG.get("budget_guard", {}).get("daily_usd", 3.0))
SOFT_STOP = int(CFG.get("budget_guard", {}).get("soft_stop_pct", 85))

CB_ERROR_RATE = float(CFG.get("circuit_breaker", {}).get("error_rate_threshold", 0.25))
CB_WINDOW_SEC = int(CFG.get("circuit_breaker", {}).get("rolling_seconds", 60))
CB_OPEN_SEC   = int(CFG.get("circuit_breaker", {}).get("rolling_seconds", 60))
CB_MIN_EVENTS = 4

API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI(title="Eudaimonia Core API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000","http://127.0.0.1:3000",
        "http://localhost:5173","http://127.0.0.1:5173",
        "http://localhost:8080","http://127.0.0.1:8080",
        "*"
    ],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class Ask(BaseModel):
    prompt: str
    mode: str | None = None

def require_auth(authorization: str | None):
    if not API_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

# logging middleware
from svc.logging_mw import MetricsLogger
app.add_middleware(MetricsLogger)

# circuit breaker
from svc.cbreaker import CircuitBreaker
CB = CircuitBreaker(
    error_rate_threshold=CB_ERROR_RATE,
    window_seconds=CB_WINDOW_SEC,
    open_seconds=CB_OPEN_SEC,
    min_events=CB_MIN_EVENTS
)

def check_soft_budget():
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = 0.0
    logp = Path("router_metrics.jsonl")
    if logp.exists():
        for line in logp.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                j = json.loads(line)
                if j.get("ts","")[:10] == today:
                    total += float(j.get("usd", 0.0))
            except Exception:
                continue
    pct = (total / BUDGET_DAILY * 100.0) if BUDGET_DAILY > 0 else 0.0
    return pct >= SOFT_STOP, pct, total

# unified error shape
@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    code_map = {401:"AUTH_REQUIRED",403:"AUTH_FORBIDDEN",429:"BUDGET_SOFT_STOP",503:"CIRCUIT_OPEN"}
    code = code_map.get(exc.status_code, "HTTP_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={"ok": False, "error": {"code": code, "message": str(exc.detail)}}
    )

@app.get("/v1/health")
def health():
    breaker = "open" if not CB.allow() else "closed"
    stop, pct, total = check_soft_budget()
    return {"ok": True, "breaker": breaker, "budget_pct": round(pct,1), "budget_today_usd": round(total, 6)}

@app.post("/v1/ask")
def ask(q: Ask, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    if not CB.allow():
        raise HTTPException(status_code=503, detail="Circuit open; please retry shortly.")
    stop, pct, total = check_soft_budget()
    if stop:
        raise HTTPException(status_code=429, detail=f"Budget soft-stop at {pct:.0f}% (${total:.2f}/{BUDGET_DAILY:.2f})")

    # test hook
    if q.prompt == "__fail__":
        CB.record(False)
        raise HTTPException(status_code=500, detail="Forced failure for breaker test.")

    try:
        res = call_model(q.prompt, mode=q.mode)  # {"text":..., "usage": {..., "usd": ...}}
        text = res.get("text","")
        usage = res.get("usage", {}) or {}
        usd = float(usage.get("usd", 0.0) or 0.0)

        headers = {"X-USD": str(usd)}
        CB.record(True)
        return JSONResponse(content={"ok": True, "output": text, "usage": usage}, headers=headers)
    except HTTPException:
        CB.record(False)
        raise
    except Exception as e:
        CB.record(False)
        return JSONResponse(status_code=500, content={"ok": False, "error": {"code":"INTERNAL_ERROR","message": str(e)}})
