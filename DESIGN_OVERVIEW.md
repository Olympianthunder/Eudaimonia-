 Project Eudaimonia — Design Overview (MVE / Architecture Only)

## Purpose
Hybrid, sovereignty‑oriented assistant that fosters flourishing:
- Local "fast‑thinker" for low‑latency reasoning
- Remote escalation for knowledge gaps (truth, breadth)
- Transparent safety (Guardian) and skill‑building (Socratic)

## System at a Glance (plain‑text diagram)
UI Shell (Web/CLI/Chat)
  -> Router API
     -> Router
        -> Local Provider  [local‑first]
        -> Remote Provider [escalate]
        -> Guardian CoT
        -> Empathy CoT
        -> BudgetGuard
        -> Telemetry Sink
Telemetry Sink -> Daily Aggregator -> Metrics Snapshot (A1 brief)

## Components (contracts only)
- Router: route(message, meta) -> { text, route: local|remote, trace, usage }
- Providers:
  - LocalProvider: generate(), is_paid() -> bool
  - RemoteProvider: generate(), is_paid() -> true
- BudgetGuard: enforces daily/per‑call caps, allow_remote_call()
- Modes: Default (knowledge‑gap aware), Empathy (structured CoT), Guardian (transparent CoT + fuse)
- Telemetry Sink: appends JSONL; nightly aggregator writes daily metrics

## Operating Posture (defaults)
- Mirror Shield; tau=0.70; Socratic 70/30; Guardian fuse=3; Trace=ON
- Daily cap $3; Per‑call $0.12; 80% alert, 100% freeze
- Remote default max_tokens=512

## Principles
- Truth over fluency: escalate on gaps; admit uncertainty
- Autonomy: 70% scaffold, 30% direct; /JUST‑TELL‑ME override
- Transparency: visible Guardian rationale; trace summaries
