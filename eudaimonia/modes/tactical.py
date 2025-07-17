"""
tactical.py
------------
Real-time defensive layer that polls ABL status each cycle
and triggers standard operating procedures (SOP) when the
defense mode escalates.

Assumes guardian.py has already created the singleton `abl`.
"""

from time import sleep
from eudaimonia.modes.guardian import abl          # SAME instance
# Import (or define) your SOP handler here
# from eudaimonia.modes.sop_handler import trigger_defense_sop

def trigger_defense_sop(status: dict) -> None:      # placeholder
    """Replace with your real SOP handler."""
    print(f"[Tactical] >>> EXECUTE SOP for mode: {status['mode']}")

# ── Main tick loop ───────────────────────────────────────────
def tick(poll_interval: float = 1.0) -> None:
    """
    Poll ABL status and invoke SOPs on ESCALATE / TERMINATE.

    Parameters
    ----------
    poll_interval : float
        Seconds between polls. Adjust per performance needs.
    """
    while True:
        status = abl.get_status()
        if status["mode"] in ("ESCALATE", "TERMINATE"):
            trigger_defense_sop(status)

        # … other tactical tasks (sensor checks, overlays) …

        sleep(poll_interval)

# ── CLI demo ────────────────────────────────────────────────
if __name__ == "__main__":
    print("[Tactical] Polling ABL every second. Ctrl-C to stop.")
    try:
        tick()
    except KeyboardInterrupt:
        print("\n[Tactical] Stopped.")

