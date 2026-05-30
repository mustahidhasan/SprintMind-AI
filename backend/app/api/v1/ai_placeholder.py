from time import perf_counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies.db import get_db
from app.services.ai_client import AIClient
from app.services.ai_request_log_service import log_ai_request

router = APIRouter(prefix='/ai', tags=['ai'])


def _client() -> AIClient:
    return AIClient(settings.ai_service_url)


@router.post('/issue/generate')
async def issue_generate(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/issue/generate', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/issue/generate',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result


@router.post('/issue/quality-score')
async def issue_quality_score(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/issue/quality-score', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/issue/quality-score',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result


@router.post('/issue/duplicate-check')
async def issue_duplicate_check(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/issue/duplicate-check', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/issue/duplicate-check',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result


@router.post('/sprint/risk-score')
async def sprint_risk_score(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/sprint/risk-score', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/sprint/risk-score',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result


@router.post('/business/impact-score')
async def business_impact_score(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/business/impact-score', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/business/impact-score',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result


@router.post('/explain')
async def explain(payload: dict, db: Session = Depends(get_db)) -> dict:
    start = perf_counter()
    result = await _client().safe_post('/explain', payload)
    log_ai_request(
        db,
        user_id=None,
        route='/explain',
        provider=settings.ai_provider_name,
        model=settings.ai_model_name,
        status='SUCCESS' if result.get('success') else 'FAILED',
        latency_ms=int((perf_counter() - start) * 1000),
        error_message=result.get('message') if not result.get('success') else None,
    )
    return result
