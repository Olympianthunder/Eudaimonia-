class BaseMode:
    name = "base"
    tone = "neutral"

    def on_activate(self, context):
        pass

    def on_deactivate(self):
        pass

    def process_request(self, request, context):
        raise NotImplementedError

    def should_trigger(self, context):
        return False
