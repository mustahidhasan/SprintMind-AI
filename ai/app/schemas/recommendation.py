from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    scoreType: str
    score: int = Field(ge=0, le=100)
    riskLevel: str
    factors: list[str] = Field(default_factory=list)
