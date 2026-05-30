from pydantic import BaseModel, Field


class GenerateIssueRequest(BaseModel):
    rawTitle: str = Field(min_length=3, max_length=300)
    rawDescription: str = Field(min_length=5, max_length=4000)
    businessGoal: str = Field(default='', max_length=500)
    projectContext: str = Field(default='', max_length=500)
    preferredIssueType: str = Field(default='Story', max_length=50)
    preferredPriority: str = Field(default='Medium', max_length=50)


class QualityScoreRequest(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    description: str = Field(min_length=5, max_length=4000)
    acceptanceCriteria: list[str] = Field(default_factory=list)
    issueType: str = Field(default='Task', max_length=50)
    priority: str = Field(default='Medium', max_length=50)
    labels: list[str] = Field(default_factory=list)


class CandidateIssue(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    description: str = Field(min_length=5, max_length=4000)


class ExistingIssue(BaseModel):
    id: str
    title: str
    description: str


class DuplicateCheckRequest(BaseModel):
    candidateIssue: CandidateIssue
    existingIssues: list[ExistingIssue] = Field(default_factory=list)
