class PredictionService:
    def risk_score(self, sprint_id: str) -> dict:
        return {"sprint_id": sprint_id, "risk_score": 0.29}
