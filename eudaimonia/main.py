from eudaimonia.core.eudaimonia import Eudaimonia

if __name__ == "__main__":
    assistant = Eudaimonia()

    test_contexts = [
        {"is_family_context": True, "request": "Check on the kids."},
        {"user_entered_tactical_command": True, "request": "Run safety protocol."},
        {"emotion_hint": "anxious", "request": "I feel overwhelmed."},
        {"request": "What's for dinner?"}
    ]

    for context in test_contexts:
        request = context.pop("request")
        response = assistant.process_request(request, context)
        print(response)
