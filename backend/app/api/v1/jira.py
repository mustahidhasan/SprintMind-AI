from fastapi import APIRouter

from app.services.jira_service import JiraService

router = APIRouter(prefix="/jira", tags=["jira"])
service = JiraService()


@router.post("/connect")
def connect_jira() -> dict:
    return service.connect()
