from fastapi import APIRouter

from app.schemas.issue import QualityScoreRequest
from app.services.quality_service import QualityService

router = APIRouter(prefix='/issue', tags=['issue'])
service = QualityService()


@router.post('/quality-score')
def quality_score(payload: QualityScoreRequest) -> dict:
    return {'success': True, 'message': 'Issue quality score generated', 'data': service.score(payload)}
