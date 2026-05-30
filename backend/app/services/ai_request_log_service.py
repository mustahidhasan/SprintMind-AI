from sqlalchemy.orm import Session

from app.models.entities import AIRequestLog


def log_ai_request(
    db: Session,
    *,
    user_id: str | None,
    route: str,
    provider: str,
    model: str,
    status: str,
    latency_ms: int,
    error_message: str | None = None,
) -> None:
    db.add(
        AIRequestLog(
            user_id=user_id,
            route=route,
            provider=provider,
            model=model,
            status=status,
            latency_ms=latency_ms,
            error_message=error_message,
        )
    )
    db.commit()
