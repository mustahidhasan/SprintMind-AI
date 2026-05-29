from fastapi import APIRouter

from app.services.business_impact_service import BusinessImpactService

router = APIRouter(prefix="/business", tags=["business"])
service = BusinessImpactService()


@router.post("/impact-score")
def business_impact_score() -> dict:
    return service.score()
