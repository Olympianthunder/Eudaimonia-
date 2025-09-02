import os
from typing import Any, Dict

def _stub(prompt: str, mode: str | None = None) -> Dict[str, Any]:
    return {"text": f"[stubbed router] {prompt}", "usage": {"model": "stub", "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "usd": 0.0}}

def call_model(prompt: str, mode: str | None = None) -> Dict[str, Any]:
    router = (os.getenv("ROUTER", "stub") or "stub").lower()
    if router == "openai":
        from .openai_provider import chat_complete
        return chat_complete(prompt, model=os.getenv("MODEL", None))
    return _stub(prompt, mode)
