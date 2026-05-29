from pydantic import BaseModel


class SprintRiskScoreRequest(BaseModel):
    sprint_id: str
