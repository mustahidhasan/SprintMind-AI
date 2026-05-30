from fastapi import APIRouter

from app.schemas.issue import DuplicateCheckRequest

router = APIRouter(prefix='/issue', tags=['issue'])


def _token_set(value: str) -> set[str]:
    return {t for t in ''.join(c.lower() if c.isalnum() else ' ' for c in value).split() if t}


@router.post('/duplicate-check')
def duplicate_check(payload: DuplicateCheckRequest) -> dict:
    candidate_tokens = _token_set(f"{payload.candidateIssue.title} {payload.candidateIssue.description}")
    matches = []
    for issue in payload.existingIssues:
        issue_tokens = _token_set(f"{issue.title} {issue.description}")
        if not candidate_tokens or not issue_tokens:
            continue
        intersection = len(candidate_tokens & issue_tokens)
        union = len(candidate_tokens | issue_tokens)
        similarity = round(intersection / union, 2) if union else 0.0
        if similarity >= 0.45:
            matches.append(
                {
                    'id': issue.id,
                    'similarityScore': similarity,
                    'reason': 'Issue text overlap indicates potential duplicate functionality.',
                }
            )

    return {
        'success': True,
        'message': 'Duplicate check completed',
        'data': {'isPotentialDuplicate': len(matches) > 0, 'matches': sorted(matches, key=lambda x: x['similarityScore'], reverse=True)},
    }
