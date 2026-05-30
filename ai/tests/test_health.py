from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    res = client.get('/api/v1/health')
    assert res.status_code == 200
    body = res.json()
    assert body['success'] is True
    assert body['data']['service'] == 'ai'
