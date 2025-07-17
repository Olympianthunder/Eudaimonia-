"""
guardian.py
------------
Monitors incoming text-based events and feeds them to the
Autonomous Battle Logic (ABL) engine for threat assessment.

This file intentionally contains only the essentials:
    • Singleton ABL instance
    • detect_event() entry point
    • escalation notice placeholder

Feel free to extend with your existing guardian routines
(e.g., sentiment analysis, logging, webhook alerts).
"""

from eudaimonia.core.abl_core import ABLCore

# ── ABL singleton ───────────────────────────────────────────
abl = ABLCore()          # shared across the whole app

# ── Public API ──────────────────────────────────────────────
def detect_event(event_text: str) -> None:
    """
    Route an incoming event (message, DM, phone transcript, etc.)
    through the Autonomous Battle Logic engine.

    Parameters
    ----------
    event_text : str
        Raw description or text content of the event.
    """
    # Early-warning flag for subtle cues
    early = any(
        phrase in event_text.lower()
        for phrase in ("passive-aggressive", "tone shift")
    )

    # Feed the event to ABL
    abl.run_protocol(event_text, early=early)

    # --------------------------------------------------------
    # Placeholder for the rest of your guardian workflow:
    #   • additional NLP / sentiment checks
    #   • persistence to risk archive
    #   • triggers for overlays, webhooks, etc.
    # --------------------------------------------------------

    # Example escalation notice (safe to remove or replace)
    status = abl.get_status()
    if status["mode"] in ("ESCALATE", "TERMINATE"):
        print(f"[Guardian] Mode escalated to {status['mode']}")
