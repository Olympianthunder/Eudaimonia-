# FastAPI entrypoint for integrated Eudaimonia Alpha
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# TODO: mount /sop, /metronome, /sms endpoints here
