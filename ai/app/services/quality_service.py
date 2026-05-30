from app.schemas.issue import QualityScoreRequest


class QualityService:
    def score(self, payload: QualityScoreRequest) -> dict:
        title_len = len(payload.title.strip())
        desc_len = len(payload.description.strip())
        has_ac = len(payload.acceptanceCriteria) > 0
        has_labels = len(payload.labels) > 0

        clarity = 20 + min(30, title_len // 3) + min(20, desc_len // 50)
        completeness = 30 + (20 if has_ac else 0) + (10 if has_labels else 0)
        testability = 30 + (25 if has_ac else 0)
        dependency = 50
        business = 50 + (10 if payload.priority.lower() in {'high', 'critical'} else 0)

        overall = int((clarity + completeness + testability + dependency + business) / 5)
        overall = max(0, min(100, overall))

        problems = []
        recommendations = []
        if not has_ac:
            problems.append('Acceptance criteria are missing')
            recommendations.append('Add clear acceptance criteria')
        if desc_len < 60:
            problems.append('Description lacks sufficient details')
            recommendations.append('Expand expected behavior and constraints')
        if not has_labels:
            problems.append('No labels provided')
            recommendations.append('Add labels for domain and component ownership')

        return {
            'overallScore': overall,
            'clarityScore': max(0, min(100, clarity)),
            'completenessScore': max(0, min(100, completeness)),
            'testabilityScore': max(0, min(100, testability)),
            'dependencyClarityScore': dependency,
            'businessValueScore': business,
            'problems': problems,
            'recommendations': recommendations,
            'confidence': 0.82,
        }
