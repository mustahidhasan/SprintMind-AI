from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/issue/generate")
@router.post("/issue/quality-score")
@router.post("/sprint/risk-score")
@router.post("/business/impact-score")
def ai_tbd() -> dict:
    return {"success": True, "message": "AI operation is TBD", "data": {"status": "TBD"}}
