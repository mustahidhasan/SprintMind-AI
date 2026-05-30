from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_sprint_risk():
    res = client.post(
        '/api/v1/sprint/risk-score',
        json={
            'sprintName': 'Sprint 12',
            'teamCapacity': 80,
            'committedPoints': 95,
            'issues': [],
        },
    )
    assert res.status_code == 200
    body = res.json()['data']
    assert 0 <= body['riskScore'] <= 100
    assert body['riskLevel'] in {'Low', 'Medium', 'High', 'Critical'}
