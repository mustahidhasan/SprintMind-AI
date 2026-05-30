from pydantic import BaseModel


class IssueImportRequest(BaseModel):
    title: str
    description: str
    sourceType: str = "MANUAL"
    priority: str = "MEDIUM"
