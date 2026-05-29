from fastapi import APIRouter

from app.schemas.recommendation import RecommendationResponse

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationResponse)
def get_recommendations() -> RecommendationResponse:
    return RecommendationResponse(recommendation="Split large issues", confidence=0.81)
