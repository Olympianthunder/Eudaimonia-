import os
from core.base_mode import BaseMode

class GuardianMode(BaseMode):
    name = "guardian_mode"
    tone = "protective"

    def should_trigger(self, context):
        return context.get("is_family_context", False)

    def process_request(self, request, context):
        response = f"[GuardianMode - reassuring, protective, slower tempo] Everything alright? I’m watching over things — {request} handled."
        os.system(f'say "{response}"')
        return response
