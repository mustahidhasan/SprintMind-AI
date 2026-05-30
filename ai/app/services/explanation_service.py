from app.schemas.recommendation import ExplainRequest


class ExplanationService:
    def explain(self, payload: ExplainRequest) -> dict:
        factors = payload.factors or ['Insufficient data provided']
        summary = f"The {payload.scoreType} score is {payload.score} ({payload.riskLevel}) based on major delivery factors."
        return {
            'summary': summary,
            'detailedExplanation': factors,
            'recommendedNextSteps': [
                'Address the highest-impact factor first',
                'Recalculate score after mitigation',
                'Track risk trend during sprint execution',
            ],
        }
