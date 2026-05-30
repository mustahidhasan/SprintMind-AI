from app.schemas.risk import SprintRiskScoreRequest


class PredictionService:
    def risk_score(self, payload: SprintRiskScoreRequest) -> dict:
        overload_ratio = 0.0
        if payload.teamCapacity > 0:
            overload_ratio = max(0.0, (payload.committedPoints - payload.teamCapacity) / payload.teamCapacity)

        blocked_high = sum(1 for i in payload.issues if i.blocked and i.priority.lower() in {'high', 'critical'})
        low_quality = sum(1 for i in payload.issues if i.qualityScore < 60)

        capacity_risk = min(100, int(50 + overload_ratio * 100))
        blocker_risk = min(100, 40 + blocked_high * 20)
        quality_risk = min(100, 30 + low_quality * 10)
        workload_risk = min(100, 20 + len(payload.issues) * 3)
        priority_risk = min(100, 20 + sum(1 for i in payload.issues if i.priority.lower() in {'high', 'critical'}) * 5)

        risk_score = int((capacity_risk + blocker_risk + quality_risk + workload_risk + priority_risk) / 5)

        if risk_score >= 85:
            risk_level = 'Critical'
        elif risk_score >= 70:
            risk_level = 'High'
        elif risk_score >= 40:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        main_factors = []
        if payload.committedPoints > payload.teamCapacity:
            main_factors.append('Committed story points exceed team capacity')
        if blocked_high:
            main_factors.append('High-priority task is blocked')
        if low_quality:
            main_factors.append('Low-quality issues increase rework risk')

        return {
            'riskLevel': risk_level,
            'riskScore': risk_score,
            'capacityRisk': capacity_risk,
            'blockerRisk': blocker_risk,
            'qualityRisk': quality_risk,
            'deliveryConfidence': max(0, 100 - risk_score),
            'mainRiskFactors': main_factors,
            'recommendations': [
                'Reduce sprint scope if overcommitted',
                'Resolve blockers within 24 hours',
                'Refine low-quality issues before implementation',
            ],
            'confidence': 0.8,
        }
