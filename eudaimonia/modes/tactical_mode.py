from eudaimonia.core.tts import speak
from eudaimonia.core.base_mode import BaseMode

class TacticalMode(BaseMode):
    name = "tactical_mode"
    tone = "straightforward"

    def should_trigger(self, context):
        return context.get("user_entered_tactical_command", False)

    def process_request(self, request, context):
        response = f"[TacticalMode - crisp, assertive, slightly faster delivery] Directive received: {request}. Executing with precision."
        speak(response)
        return response
