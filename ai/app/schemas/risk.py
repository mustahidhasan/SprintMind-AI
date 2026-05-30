from pydantic import BaseModel, Field


class SprintIssue(BaseModel):
    id: str
    title: str
    priority: str = 'Medium'
    status: str = 'To Do'
    storyPoints: int = 0
    assignee: str | None = None
    blocked: bool = False
    qualityScore: int = 50


class SprintRiskScoreRequest(BaseModel):
    sprintName: str
    teamCapacity: int = Field(ge=0)
    committedPoints: int = Field(ge=0)
    issues: list[SprintIssue] = Field(default_factory=list)


class BusinessImpactScoreRequest(BaseModel):
    title: str
    description: str
    priority: str = 'Medium'
    customerFacing: bool = False
    releaseCritical: bool = False
    blocked: bool = False
    delayRisk: str = 'Medium'
