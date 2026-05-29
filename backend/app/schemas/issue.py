from pydantic import BaseModel


class IssueAnalysisRequest(BaseModel):
    summary: str
    description: str


class IssueDraftResponse(BaseModel):
    title: str
    description: str
    acceptance_criteria: list[str]
