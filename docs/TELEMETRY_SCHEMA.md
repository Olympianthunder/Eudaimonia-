# Telemetry & Briefs (Schema + Aggregation)

## Per-Call Log — router_metrics.jsonl (one JSON per line)
Fields:
- ts (ISO-8601 UTC)
- route ("local" | "remote")
- mode
- confidence (float)
- topic_domain
- safety_class
- ttft_ms
- tpot_ms
- tokens_in
- tokens_out
- usd (0.00 for local)

Example line:
{"ts":"2025-08-08T23:11:02Z","route":"local","mode":"default","confidence":0.82,"topic_domain":"coding","safety_class":"low","ttft_ms":180,"tpot_ms":22,"tokens_in":120,"tokens_out":180,"usd":0.00}

## Nightly Aggregator Output — metrics_daily.json
{
  "date": "2025-08-08",
  "remote_usage_7d_pct": 64.0,
  "mean_daily_remote_pct_7d": 57.3,
  "spend_today_usd": 2.49,
  "spend_7d_usd": 11.83,
  "ttft_p95_local_ms": 210,
  "ttft_p95_remote_ms": 420,
  "tpot_p95_local_ms": 23,
  "tpot_p95_remote_ms": 18
}

## Calculations
- remote_usage_7d_pct = (remote_turns / all_turns) * 100 over the last 7 days.
- p95 computed per route bucket (local vs remote).

## A1 Daily Brief (6:00 PM CT)
- Remote % (7d), trend arrow, alert if > 60%.
- Spend today vs cap; per-call violations.
- Notes: top domains, Guardian triggers, fuse status.

## Retention
- Raw per-call logs 14 days; daily snapshots 90 days.