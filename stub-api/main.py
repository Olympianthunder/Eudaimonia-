from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class ConfirmRequest(BaseModel):
    sop_id: str
    decision: str

app = FastAPI()

@app.post("/sop/confirm")
def confirm(req: ConfirmRequest):
    return {"status": f"DRY_RUN: {req.decision} received for {req.sop_id}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
