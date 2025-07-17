# 🛡️ Autonomous Battle Logic – Master Directive  
*(Codename: BattleLogic 1.0 “ThornsUp”)*

---

## PURPOSE  
Provide a modular, deterministic engine for emotional-threat detection, defensive-posture selection, and incident logging.

* **Pillar 1 – Strategic Doctrine**  
  Sun Tzu · Jedi Code · Lightsaber Forms

* **Pillar 2 – Technical Soundness**  
  Config-driven FSM, unit-tested, side-effect-free.

* **Pillar 3 – Robust Transparency**  
  Structured logs for legal and analytic review.

---

## STRATEGIC MAP

| Threat Level | Defense Mode | Lightsaber Form     | Doctrine Tagline           |
|--------------|--------------|---------------------|----------------------------|
| **LOW**                    | OBSERVE    | Form I – Shii-Cho | Balanced Watch            |
| **LOW / MOD (early)**      | **INTERCEPT** | Form III – Soresu | Guard & Wait (stealth)    |
| **MODERATE**               | DEFLECT    | Form V – Shien    | Redirect Force            |
| **HIGH**                   | ESCALATE   | Form IV – Ataru   | Forward Momentum          |
| **CRITICAL**               | TERMINATE  | Form VII – Vaapad | Legal Severance           |

---

## TECHNICAL DOCTRINE

1. **Single Source of Truth** → `abl_config.json` drives keywords & form map.  
2. **Finite-State Machine** → ABLCore decides; other subsystems act.  
3. **Fail-Safe Defaults** → Unknown inputs default to **OBSERVE**.  
4. **Side-Effect Isolation** → No external calls inside `abl_core.py`.  
5. **Full Traceability** → Each state change logged (`timestamp`, `threat`, `notes`).

---

## INTEGRATION POINTS

| Subsystem          | Trigger → Call                              | Data Flow                                 |
|--------------------|---------------------------------------------|-------------------------------------------|
| **guardian.py**    | `detect_event()` → `abl.run_protocol()`     | raw text + `early` flag                   |
| **tactical.py**    | poll `abl.get_status()`                    | state / mode → SOP handler                |
| **codex_engine**   | mode-change event bus → narrative overlay  | mode → `form_map` label                   |
| **memory_store**   | flush `abl.memory.events`                  | JSON / SQLite persistence                 |
| **discord_alerts** *(optional)* | subscribe to log bus         | webhook JSON                              |

---

## MODE BEHAVIOUR

* **OBSERVE** – passive monitoring.  
* **INTERCEPT** – stealth stance; shorten replies, neutral tone, no tip-off.  
* **DEFLECT** – active redirection; reinforce boundaries.  
* **ESCALATE** – assert boundaries; prep legal fallback.  
* **TERMINATE** – cease contact; trigger legal & safety protocols.

---

## QUICK CLI DEMO

```python
from eudaimonia.core.abl_core import ABLCore
abl = ABLCore()
abl.run_protocol("passive-aggressive DM", early=True)
# ➜ THREAT=LOW   MODE=INTERCEPT

