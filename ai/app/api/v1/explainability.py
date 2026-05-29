from fastapi import APIRouter

from app.schemas.recommendation import ExplainRequest
from app.services.explanation_service import ExplanationService

router = APIRouter(prefix="/explain", tags=["explain"])
service = ExplanationService()


@router.post("")
def explain(payload: ExplainRequest) -> dict:
    return service.explain(payload.message)
