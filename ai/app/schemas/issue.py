from pydantic import BaseModel


class GenerateIssueRequest(BaseModel):
    requirement: str
