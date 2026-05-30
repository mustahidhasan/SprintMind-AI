from app.schemas.risk import BusinessImpactScoreRequest


class BusinessImpactService:
    def score(self, payload: BusinessImpactScoreRequest) -> dict:
        score = 20
        if payload.customerFacing:
            score += 25
        if payload.releaseCritical:
            score += 25
        if payload.priority.lower() in {'high', 'critical'}:
            score += 15
        if payload.delayRisk.lower() in {'high', 'critical'}:
            score += 10
        if payload.blocked:
            score += 10

        score = max(0, min(100, score))

        if score >= 85:
            level = 'Critical'
        elif score >= 70:
            level = 'High'
        elif score >= 40:
            level = 'Medium'
        else:
            level = 'Low'

        return {
            'impactLevel': level,
            'impactScore': score,
            'costOfDelay': 'High' if score >= 70 else 'Medium' if score >= 40 else 'Low',
            'customerImpact': 'High' if payload.customerFacing else 'Medium',
            'releaseRisk': 'High' if payload.releaseCritical else 'Medium',
            'reasoning': [
                'The issue is customer-facing' if payload.customerFacing else 'The issue has indirect customer visibility',
                'The issue is release-critical' if payload.releaseCritical else 'The issue is not release-critical',
                f"Delay risk is {payload.delayRisk}",
            ],
            'recommendedAction': [
                'Assign senior engineer',
                'Add QA test coverage early',
                'Track this issue daily until completion',
            ],
            'confidence': 0.84,
        }
