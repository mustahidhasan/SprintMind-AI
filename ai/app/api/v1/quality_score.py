from fastapi import APIRouter

from app.services.quality_service import QualityService

router = APIRouter(prefix="/issue", tags=["issue"])
service = QualityService()


@router.post("/quality-score")
def quality_score() -> dict:
    return service.score()
