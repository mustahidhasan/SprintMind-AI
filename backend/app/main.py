from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1 import ai_placeholder, approvals, auth, dashboard, health, issues, jira
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.entities import User

configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(health.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(jira.router, prefix=api_prefix)
app.include_router(dashboard.router, prefix=api_prefix)
app.include_router(issues.router, prefix=api_prefix)
app.include_router(approvals.router, prefix=api_prefix)
app.include_router(ai_placeholder.router, prefix=api_prefix)


@app.on_event("startup")
def ensure_default_admin_user() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@gmail.com").first()
        if not existing:
            db.add(
                User(
                    name="Admin",
                    email="admin@gmail.com",
                    password_hash=hash_password("admin@gmail.com"),
                )
            )
            db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()
