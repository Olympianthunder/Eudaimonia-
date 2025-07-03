from eudaimonia.core.tts import speak
from eudaimonia.core.base_mode import BaseMode

class DefaultMode(BaseMode):
    name = "default"
    tone = "bahamian_female_freeport"

    def on_activate(self, context):
        print("Default mode activated. Speaking in Freeport Bahamian tone.")

    def process_request(self, request, context):
        response = f"[DefaultMode - Bahamian Voice] I get you, {request}. Let’s handle it, aye."
        speak(response)
        return response
