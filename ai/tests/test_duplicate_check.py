from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_duplicate_check():
    res = client.post(
        '/api/v1/issue/duplicate-check',
        json={
            'candidateIssue': {'title': 'Export dashboard CSV', 'description': 'Need csv export'},
            'existingIssues': [
                {'id': '1', 'title': 'CSV export for dashboard', 'description': 'Allow csv export'},
            ],
        },
    )
    assert res.status_code == 200
    assert res.json()['success'] is True
