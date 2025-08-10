# Eudaimonia — Architecture Docs (MVE)

This folder holds the **architecture-only** blueprint for the hybrid, sovereignty-oriented assistant.  
No code is executed; safe to review/merge on mobile.

## Contents
- DESIGN_OVERVIEW.md — system picture & components
- ROUTING_MATRIX.md — deterministic routing rules (τ=0.70; gap domains)
- MODES_SPEC.md — Default/Empathy/Guardian CoT skeletons
- BUDGET_POLICY.md — caps, alerts, shim-guard
- TELEMETRY_SCHEMA.md — per-call JSONL + nightly snapshot
- FORMAT_CI.md — YAML-first, mobile-safe CI plan

## Status
- Posture: Mirror Shield • Socratic 70/30 • Guardian fuse=3 • Trace=ON
- Caps: $3/day, $0.12/call (alert 80%, freeze 100%)
- Remote default: max_tokens=512
- 120B node: essential (deferred until 5–7 days clean telemetry)

## Next (no code yet)
1) Open a PR titled “docs: arch blueprint v1”.
2) Collect review comments; adjust docs only.
3) After merge, add YAML stubs in `codex/modes/` (still non-runtime).

*Principle: Truth > fluency • Autonomy • Transparency.*