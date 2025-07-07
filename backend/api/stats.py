from fastapi import APIRouter

from telemetry.metrics import get_stats

router = APIRouter()


@router.get("/stats")
async def stats():
    return get_stats()
