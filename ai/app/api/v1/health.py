from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix='/health', tags=['health'])


@router.get('')
def health() -> dict:
    return {
        'success': True,
        'message': 'SprintMind AI service is running',
        'data': {
            'status': 'ok',
            'service': 'ai',
            'version': settings.app_version,
            'provider': settings.model_provider,
            'model': settings.llm_model_name,
        },
    }
