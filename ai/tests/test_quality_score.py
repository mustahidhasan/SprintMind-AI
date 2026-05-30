from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_quality_score():
    res = client.post(
        '/api/v1/issue/quality-score',
        json={
            'title': 'Fix dashboard issue',
            'description': 'Dashboard fails to load reports for managers in filter mode.',
            'acceptanceCriteria': ['Report loads in under 2 seconds'],
            'issueType': 'Task',
            'priority': 'Medium',
            'labels': ['dashboard'],
        },
    )
    assert res.status_code == 200
    body = res.json()['data']
    assert 0 <= body['overallScore'] <= 100
