from ..core.tts import speak
from ..core.base_mode import BaseMode

class EmpathyMode(BaseMode):
    name = "empathy_mode"
    tone = "supportive"

    def should_trigger(self, context):
        return context.get("emotion_hint") in {"sad", "anxious"}

    def process_request(self, request, context):
        response = (
            f"[EmpathyMode - gentle, warm, emotionally tuned phrasing] I hear you,"
            f" and I’m here. Let’s take this one step at a time: {request}."
        )
        speak(response)
        return response
