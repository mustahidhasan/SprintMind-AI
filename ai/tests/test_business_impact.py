from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_business_impact():
    res = client.post(
        '/api/v1/business/impact-score',
        json={
            'title': 'Payment validation API',
            'description': 'Implement payment validation',
            'priority': 'High',
            'customerFacing': True,
            'releaseCritical': True,
            'blocked': False,
            'delayRisk': 'High',
        },
    )
    assert res.status_code == 200
    body = res.json()['data']
    assert 0 <= body['impactScore'] <= 100
    assert body['impactLevel'] in {'Low', 'Medium', 'High', 'Critical'}
