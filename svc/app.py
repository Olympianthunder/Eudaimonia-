from fastapi import FastAPI
from pydantic import BaseModel
try:
    from eudaimonia.core.router import call_model
except ImportError:
    def call_model(text, mode=None):
        return f"[stubbed router] {text}"

app = FastAPI()

class Ask(BaseModel):
    prompt: str
    mode: str | None = None

@app.post("/v1/ask")
def ask(q: Ask):
    out = call_model(q.prompt, mode=q.mode)
    return {"ok": True, "output": out}
