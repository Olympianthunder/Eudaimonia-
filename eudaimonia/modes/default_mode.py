from ..core.tts import speak
from ..core.base_mode import BaseMode
from ..core.storage import get_recent_events


class DefaultMode(BaseMode):
    name = "default"
    tone = "bahamian_female_freeport"

    def on_activate(self, context):
        events = get_recent_events("empathy_check", 1)
        if events:
            mood = events[0]["data"].get("mood")
            print(f"Welcome back. Last mood was {mood}.")
        else:
            print("Default mode activated. Speaking in Freeport Bahamian tone.")

    def process_request(self, request, context):
        response = f"[DefaultMode - Bahamian Voice] I get you, {request}. Let’s handle it, aye."
        speak(response)
        return response
