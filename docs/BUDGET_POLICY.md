# Budget Policy (Caps, Alerts, Shim-Guard)

## Caps
- Daily: $3.00
- Per-call: $0.12
- Alert at 80% ($2.40); Freeze at 100% ($3.00)

## Behaviors
- Pre-call: if a remote call would exceed per-call ceiling, warn or truncate (prefer truncate via max_tokens=512).
- At 80%: surface soft warning in overlay and daily brief.
- At 100%: freeze paid endpoints.

## Shim-Guard
- After freeze, block any provider that is paid:
  - provider.is_paid() == true, or
  - endpoint host matches api.openai.com (or another known paid host).
- Return bounded local reply: “Budget cap reached; paid endpoint blocked; start a true local server or wait for reset.”

## Controls
- /budget daily $N percall $M
- /escalate on|off|auto  (respects budget guard)

## Acceptance Criteria
- After 100% cap, 0 paid calls recorded that day.
- Per-call > $0.12 attempts are truncated or require explicit confirm.