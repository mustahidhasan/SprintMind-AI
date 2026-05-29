class ReportService:
    def sprint_health(self) -> dict:
        return {"overall": "stable", "blocked_issues": 0, "at_risk_issues": 1}
