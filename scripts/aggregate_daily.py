#!/usr/bin/env python3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG = Path("router_metrics.jsonl")
OUT = Path("metrics_daily.json")

def load_records(days=7):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                j = json.loads(line)
                ts = j.get("ts", "1970-01-01T00:00:00Z")[:10]
                if ts >= cutoff.strftime("%Y-%m-%d"):
                    out.append(j)
            except Exception:
                continue
    return out

def main():
    recs = load_records()
    total = len(recs)
    remote = sum(1 for r in recs if r.get("route") == "remote")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    spend_today = float(
        sum(r.get("usd", 0.0) for r in recs if r.get("ts", "")[:10] == today)
    )
    out = {
        "date": today,
        "remote_usage_7d_pct": round((remote / total * 100.0) if total else 0.0, 1),
        "spend_today_usd": round(spend_today, 2),
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out))

if __name__ == "__main__":
    main()

