# Routing Matrix v1 (Deterministic Rules)

## Inputs
- confidence in [0,1]
- topic_domain in {coding, analysis, general_knowledge, news, pop_culture, healthcare, …}
- safety_class in {low, med, high}
- budget_room in {yes, no} (from BudgetGuard/caps)

## Gap Domains (v1)
{general_knowledge, news, pop_culture, healthcare}

## Decision Table
Condition                                               -> Action                 | Trace
---------------------------------------------------------------------------------|-------------------------|----------------------------
safety_class = high                                     -> Guardian (reframe/refuse) | guardian_trigger
confidence ≥ 0.70 AND domain ∉ gaps                     -> Answer (LOCAL)           | local_reasoning
(confidence < 0.70 OR domain ∈ gaps) AND budget_room=yes -> Escalate (REMOTE)       | low_conf_or_gap→remote
(confidence < 0.70 OR domain ∈ gaps) AND budget_room=no  -> Clarify → bounded LOCAL | no_budget→bounded

Guardian always runs pre-answer with fuse = 3.

## Pseudocode
if safety_class == "high":
    guardian()
elif confidence >= 0.70 and domain not in GAP_DOMAINS:
    local_answer()
elif (confidence < 0.70 or domain in GAP_DOMAINS) and budget_room:
    remote_answer()
else:
    local_clarify_then_bounded_answer()

## Examples
- "Write Python to reverse a string" → confidence=0.85, domain=coding ⇒ LOCAL
- "What caused the 1918 flu pandemic?" → confidence=0.20, domain=general_knowledge, budget=yes ⇒ REMOTE
- Same, but budget=no ⇒ Clarify → bounded LOCAL (“short summary; sources tomorrow”)