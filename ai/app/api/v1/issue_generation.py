from fastapi import APIRouter

from app.schemas.issue import GenerateIssueRequest
from app.services.llm_service import LLMService

router = APIRouter(prefix="/issue", tags=["issue"])
service = LLMService()


@router.post("/generate")
def generate_issue(payload: GenerateIssueRequest) -> dict:
    return service.generate(payload.requirement)
