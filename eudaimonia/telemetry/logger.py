import json, os, time
from pathlib import Path

LOG_PATH = Path(os.getenv("EUDA_TELEM_LOG", "router_metrics.jsonl"))

def log_call(*, route: str, mode: str, confidence: float, topic_domain: str,
             safety_class: str, ttft_ms: int|None=None, tpot_ms: int|None=None,
             tokens_in: int|None=None, tokens_out: int|None=None, usd: float=0.0):
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "route": route, "mode": mode, "confidence": confidence,
        "topic_domain": topic_domain, "safety_class": safety_class,
        "ttft_ms": ttft_ms, "tpot_ms": tpot_ms,
        "tokens_in": tokens_in, "tokens_out": tokens_out, "usd": usd,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")
