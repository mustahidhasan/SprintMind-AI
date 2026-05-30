from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_issue_generate():
    res = client.post(
        '/api/v1/issue/generate',
        json={
            'rawTitle': 'Need login',
            'rawDescription': 'User should login with email and password',
            'businessGoal': '',
            'projectContext': '',
            'preferredIssueType': 'Story',
            'preferredPriority': 'Medium',
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body['success'] is True
    assert 0 <= body['data']['confidence'] <= 1
