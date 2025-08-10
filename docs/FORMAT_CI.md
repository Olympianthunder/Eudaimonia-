# Format & CI Plan (YAML-First, Mobile-Safe)

## Why
Mobile editors add smart quotes/newlines that break JSONL. Author in YAML, lint YAML only in PR-1, generate JSON/JSONL later on laptop.

## Layout (proposed)
codex/
  modes/
    default.yaml
    empathy.yaml
    guardian.yaml
  schemas/
    modes.schema.yaml
docs/
  DESIGN_OVERVIEW.md
  ROUTING_MATRIX.md
  MODES_SPEC.md
  BUDGET_POLICY.md
  TELEMETRY_SCHEMA.md
  FORMAT_CI.md

## YAML Stubs (author first)
codex/modes/default.yaml
version: 0.1
stance: Mirror Shield
socratic_ratio: "70/30"
routing:
  tau: 0.70
  gap_domains: [general_knowledge, news, pop_culture, healthcare]
guardian:
  fuse: 3
trace: true

codex/modes/empathy.yaml
version: 0.1
cot:
  - detect_emotion
  - validate
  - clarify
  - reflect
  - offer_support
  - growth_nudger_optional

codex/modes/guardian.yaml
version: 0.1
cot:
  - state_trigger
  - explain_analysis
  - conclude_and_act
fuse: 3
logging_fields: [risk_level, reason_codes, fuse_count]

## CI for PR-1
- Lint YAML against modes.schema.yaml.
- No JSON/JSONL generation in CI for this PR.
- (Optional) reject non-ASCII.

## Later (on laptop)
- Add tiny generator: YAML -> JSONL for runtime.
- Flip CI to validate generated artifacts when ready.