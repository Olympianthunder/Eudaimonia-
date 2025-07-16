# ─── Autonomous Battle Logic Core (BattleLogic_1.0_ThornsUp) ────────────────
"""
ABLCore is Eudaimonia’s emotional-threat engine.

Strategic doctrine:
    • Sun Tzu   – anticipate & shape
    • Jedi Code – serenity before action
    • Lightsaber Forms – choose form to fit the moment

Technical doctrine:
    • Config-driven FSM (abl_config.json)
    • Deterministic, side-effect-free
    • Structured logs for legal / analytic review
"""

from __future__ import annotations
import datetime
import json
from enum import Enum
from pathlib import Path
from typing import Optional

# ─── Enum Definitions ──────────────────────────────────────────────────────
class ThreatLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class DefenseMode(Enum):
    OBSERVE = "observe"      # passive monitoring
    INTERCEPT = "intercept"  # stealth posture (Form III – Soresu)
    DEFLECT = "deflect"      # active redirection  (Form V – Shien)
    ESCALATE = "escalate"    # direct engagement   (Form IV – Ataru)
    TERMINATE = "terminate"  # legal cut-off       (Form VII – Vaapad)


class EmotionalState(Enum):
    CALM = "calm"
    ALERT = "alert"
    TRIGGERED = "triggered"
    DETACHED = "detached"
    RECOVERING = "recovering"

# ─── Memory Log ────────────────────────────────────────────────────────────
class ABLMemoryLog:
    """In-memory rolling log; persisted elsewhere by memory_store.py."""
    def __init__(self) -> None:
        self.events: list[dict] = []

    def log_event(self, ts: str, threat: ThreatLevel, notes: str) -> None:
        self.events.append(
            {"timestamp": ts, "threat_level": threat.name, "notes": notes}
        )

    def get_last(self) -> Optional[dict]:
        return self.events[-1] if self.events else None

# ─── Core Engine ───────────────────────────────────────────────────────────
class ABLCore:
    """Assess threat → select defense mode → log event."""
    CONFIG_PATH = Path(__file__).with_name("abl_config.json")

    def __init__(self, user_name: str = "Thunder") -> None:
        self.user_name = user_name
        self.state = EmotionalState.CALM
        self.mode: DefenseMode = DefenseMode.OBSERVE
        self.memory = ABLMemoryLog()
        self._config = self._load_config()

    # ── Public API ────────────────────────────────────────────────────────
    def run_protocol(self, event_text: str, *, early: bool = False) -> None:
        """
        Main entry: evaluate `event_text`, update mode, log outcome.

        Args:
            event_text: raw text describing the trigger.
            early: set True when guardian.py flags an early-warning pattern.
        """
        now = datetime.datetime.utcnow().isoformat()
        threat = self._assess_threat(event_text)
        self._update_mode(threat, early=early)
        self.memory.log_event(now, threat, event_text)
        print(f"[{now}] THREAT={threat.name:>8}  →  MODE={self.mode.name}")

    def get_status(self) -> dict:
        """Lightweight status snapshot for overlays / polling."""
        return {
            "state": self.state.name,
            "mode": self.mode.name,
            "last_event": self.memory.get_last(),
        }

    # ── Internal helpers ──────────────────────────────────────────────────
    def _load_config(self) -> dict:
        if self.CONFIG_PATH.exists():
            return json.loads(self.CONFIG_PATH.read_text())
        # Fallback defaults
        return {
            "keywords": {
                "CRITICAL": ["threaten", "harm", "legal action"],
                "HIGH": ["manipulation", "coercion"],
                "MODERATE": ["verbal attack", "gaslight"],
                "LOW": ["passive-aggressive"],
            }
        }

    def _assess_threat(self, text: str) -> ThreatLevel:
        """Keyword-based scan; guardian.py may provide NLP score later."""
        lowered = text.lower()
        for level in ("CRITICAL", "HIGH", "MODERATE", "LOW"):
            if any(kw in lowered for kw in self._config["keywords"].get(level, [])):
                return ThreatLevel[level]
        return ThreatLevel.LOW

    def _update_mode(self, threat: ThreatLevel, *, early: bool) -> None:
        """Deterministic mode selection; early flag triggers INTERCEPT."""
        if early and threat in {ThreatLevel.LOW, ThreatLevel.MODERATE}:
            self.mode = DefenseMode.INTERCEPT
            return

        self.mode = {
            ThreatLevel.LOW: DefenseMode.OBSERVE,
            ThreatLevel.MODERATE: DefenseMode.DEFLECT,
            ThreatLevel.HIGH: DefenseMode.ESCALATE,
            ThreatLevel.CRITICAL: DefenseMode.TERMINATE,
        }[threat]


# ─── CLI Demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    abl = ABLCore()
    abl.run_protocol("passive-aggressive DM", early=True)          # → INTERCEPT
    abl.run_protocol("coercion via phone call demanding money")    # → ESCALATE
    print(abl.get_status())

