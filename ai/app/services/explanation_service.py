class ExplanationService:
    def explain(self, message: str) -> dict:
        return {"explanation": f"Reasoning for: {message}"}
