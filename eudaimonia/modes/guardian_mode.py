from ..core.tts import speak
from ..core.base_mode import BaseMode
from ..core.rule_engine import should_trigger_guardian

class GuardianMode(BaseMode):
    name = "guardian_mode"
    tone = "protective"

    def should_trigger(self, context):
        text = context.get("last_user_message", "")
        return should_trigger_guardian(text, context)

    def process_request(self, request, context):
        response = (
            f"[GuardianMode - reassuring, protective, slower tempo] Everything"
            f" alright? I’m watching over things — {request} handled."
        )
        speak(response)
        return response
