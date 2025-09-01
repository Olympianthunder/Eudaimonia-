from pathlib import Path
import os, json
import yaml
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

try:
    from eudaimonia.core.router import call_model
except ImportError:
    def call_model(text, mode=None): return f"[stubbed router] {text}"

# --- load config if present ---
CFG = {}
cfg_path = Path("config/router.yaml")
if cfg_path.exists():
    CFG = yaml.safe_load(cfg_path.read_text())
BUDGET_DAILY = float(CFG.get("budget_guard", {}).get("daily_usd", 3.0))
SOFT_STOP = int(CFG.get("budget_guard", {}).get("soft_stop_pct", 85))

# circuit breaker knobs (fall back to sane defaults)
CB_ERROR_RATE = float(CFG.get("circuit_breaker", {}).get("error_rate_threshold", 0.25))
CB_WINDOW_SEC = int(CFG.get("circuit_breaker", {}).get("rolling_seconds", 60))
CB_OPEN_SEC   = int(CFG.get("circuit_breaker", {}).get("rolling_seconds", 60))
CB_MIN_EVENTS = 4

# --- bearer auth (optional; enabled if API_TOKEN is set) ---
API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI()

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

# --- logging middleware (append to router_metrics.jsonl) ---
from svc.logging_mw import MetricsLogger
app.add_middleware(MetricsLogger)

# --- circuit breaker ---
from svc.cbreaker import CircuitBreaker
CB = CircuitBreaker(
    error_rate_threshold=CB_ERROR_RATE,
    window_seconds=CB_WINDOW_SEC,
    open_seconds=CB_OPEN_SEC,
    min_events=CB_MIN_EVENTS,
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
                if j.get("ts", "")[:10] == today:
                    total += float(j.get("usd", 0.0))
            except Exception:
                continue
    pct = (total / BUDGET_DAILY * 100.0) if BUDGET_DAILY > 0 else 0.0
    return pct >= SOFT_STOP, pct, total

@app.post("/v1/ask")
def ask(q: Ask, authorization: str | None = Header(default=None)):
    require_auth(authorization)

    # breaker gate: if open, refuse early
    if not CB.allow():
        raise HTTPException(status_code=503, detail="Circuit open; please retry shortly.")

    # budget guard
    stop, pct, total = check_soft_budget()
    if stop:
        raise HTTPException(
            status_code=429,
            detail=f"Budget soft-stop at {pct:.0f}% (${total:.2f}/{BUDGET_DAILY:.2f})"
        )

    # forced failure path for testing breaker
    if q.prompt == "__fail__":
        CB.record(False)
        raise HTTPException(status_code=500, detail="Forced failure for breaker test.")

    try:
        out = call_model(q.prompt, mode=q.mode)
        CB.record(True)
        return {"ok": True, "output": out}
    except Exception:
        CB.record(False)
        raise
