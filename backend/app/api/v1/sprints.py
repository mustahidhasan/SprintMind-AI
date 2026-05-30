from fastapi import APIRouter, Depends
from time import perf_counter
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.entities import RiskPrediction, User
from app.services.ai_client import AIClient
from app.services.ai_request_log_service import log_ai_request

router = APIRouter(prefix='/sprints', tags=['sprints'])


@router.post('/{sprint_id}/risk-score')
async def sprint_risk_score(
    sprint_id: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> dict:
    start = perf_counter()
    payload = {
        'sprintName': sprint_id,
        'teamCapacity': 80,
        'committedPoints': 80,
        'issues': [],
    }
    result = await AIClient(settings.ai_service_url).safe_post('/sprint/risk-score', payload)
    if result.get("success") and result.get("data"):
        data = result["data"]
        db.add(
            RiskPrediction(
                issue_draft_id=None,
                sprint_id=sprint_id,
                risk_type="SPRINT",
                risk_level=data.get("riskLevel", "Low"),
                risk_score=data.get("riskScore", 0),
                main_risk_factors=data.get("mainRiskFactors", []),
                recommendations=data.get("recommendations", []),
                confidence=data.get("confidence", 0.0),
            )
        )
        db.commit()
    log_ai_request(
        db,
        user_id=_current_user.id,
        route='/sprint/risk-score',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result
