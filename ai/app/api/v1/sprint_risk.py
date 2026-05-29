from fastapi import APIRouter

from app.schemas.risk import SprintRiskScoreRequest
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/sprint", tags=["sprint"])
service = PredictionService()


@router.post("/risk-score")
def sprint_risk_score(payload: SprintRiskScoreRequest) -> dict:
    return service.risk_score(payload.sprint_id)
