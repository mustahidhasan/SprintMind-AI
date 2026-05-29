from pydantic import BaseModel


class SprintRiskRequest(BaseModel):
    sprint_id: str


class SprintRiskResponse(BaseModel):
    sprint_id: str
    risk_score: float
