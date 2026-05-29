from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import approvals, auth, health, issues, jira, recommendations, reports, sprints
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(health.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(jira.router, prefix=api_prefix)
app.include_router(issues.router, prefix=api_prefix)
app.include_router(sprints.router, prefix=api_prefix)
app.include_router(recommendations.router, prefix=api_prefix)
app.include_router(approvals.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
