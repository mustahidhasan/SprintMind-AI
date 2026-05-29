class LLMService:
    def generate(self, requirement: str) -> dict:
        return {"title": requirement[:72], "description": requirement}
