from fastapi import APIRouter

from app.schemas.sprint import SprintRiskRequest, SprintRiskResponse

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post("/risk", response_model=SprintRiskResponse)
def sprint_risk(payload: SprintRiskRequest) -> SprintRiskResponse:
    return SprintRiskResponse(sprint_id=payload.sprint_id, risk_score=0.22)
