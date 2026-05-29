from fastapi import APIRouter

from app.schemas.issue import IssueAnalysisRequest, IssueDraftResponse

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("/analyze")
def analyze_issue(payload: IssueAnalysisRequest) -> dict:
    return {"quality": "good", "summary": payload.summary}


@router.post("/create-draft", response_model=IssueDraftResponse)
def create_draft(payload: IssueAnalysisRequest) -> IssueDraftResponse:
    return IssueDraftResponse(
        title=payload.summary,
        description=payload.description,
        acceptance_criteria=["Criterion 1", "Criterion 2"],
    )


@router.post("/approve")
def approve_issue() -> dict:
    return {"status": "approved"}
