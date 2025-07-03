from fastapi.testclient import TestClient
from api.main import app


def test_metrics_endpoint():
    client = TestClient(app)
    resp = client.get('/api/metrics')
    assert resp.status_code == 200
    data = resp.json()
    assert data['active_members'] == 120
    assert data['inactive_members'] == 30
    assert data['total_members'] == 150
