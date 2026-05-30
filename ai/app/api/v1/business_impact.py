from fastapi import APIRouter

from app.schemas.risk import BusinessImpactScoreRequest
from app.services.business_impact_service import BusinessImpactService

router = APIRouter(prefix='/business', tags=['business'])
service = BusinessImpactService()


@router.post('/impact-score')
def business_impact_score(payload: BusinessImpactScoreRequest) -> dict:
    return {'success': True, 'message': 'Business impact score generated', 'data': service.score(payload)}
