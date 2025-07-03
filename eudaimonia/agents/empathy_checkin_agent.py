"""Agent that records user emotional check-ins."""

from ..core.storage import append_event


class EmpathyCheckinAgent:
    """Log empathy-related events."""

    def check_in(self, mood: str) -> str:
        """Record the provided mood and return confirmation."""
        append_event("empathy_check", {"mood": mood})
        return "Mood logged"
