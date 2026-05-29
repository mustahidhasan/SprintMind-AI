from fastapi import FastAPI

from app.api.v1 import (
    business_impact,
    duplicate_check,
    explainability,
    health,
    issue_generation,
    quality_score,
    sprint_risk,
)
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
api_prefix = "/api/v1"

app.include_router(health.router, prefix=api_prefix)
app.include_router(issue_generation.router, prefix=api_prefix)
app.include_router(quality_score.router, prefix=api_prefix)
app.include_router(duplicate_check.router, prefix=api_prefix)
app.include_router(sprint_risk.router, prefix=api_prefix)
app.include_router(business_impact.router, prefix=api_prefix)
app.include_router(explainability.router, prefix=api_prefix)
