from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    return {"success": True, "status": "ok", "service": "backend"}
