from fastapi import FastAPI, HTTPException

from .core import tts, storage
from .core.eudaimonia import Eudaimonia
from .core.mode_manager import ModeManager

assistant = Eudaimonia()
mode_manager: ModeManager = assistant.mode_manager

app = FastAPI()


@app.post("/speak")
async def speak(payload: dict):
    text = payload.get("text")
    if not isinstance(text, str):
        raise HTTPException(status_code=400, detail="text field required")
    tts.speak(text)
    return {"status": "ok"}


@app.post("/mode")
async def switch_mode(payload: dict):
    mode = payload.get("mode")
    if not isinstance(mode, str):
        raise HTTPException(status_code=400, detail="mode field required")
    changed = mode_manager.switch_mode(mode)
    return {"active_mode": mode_manager.current_mode.name, "changed": changed}


@app.get("/log")
async def get_log(type: str, limit: int = 10):
    events = storage.get_recent_events(type, limit)
    return events
