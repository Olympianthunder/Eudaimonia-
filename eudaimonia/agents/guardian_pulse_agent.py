"""Placeholder Guardian Pulse Agent."""

from ..core.storage import append_event


class GuardianPulseAgent:
    """Simple health monitoring agent."""

    def check_pulse(self):
        """Return a dummy status string and log the event."""
        status = "Pulse normal"
        append_event("guardian_check", {"status": status})
        return status
