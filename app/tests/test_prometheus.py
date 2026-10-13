from fastapi.testclient import TestClient

from app.api import app
from app.prometheus_metrics import update_gauges


def test_prometheus_endpoint_exposes_agent_metrics():
    update_gauges(
        {
            "hostname": "test",
            "cpu": {"percent": 12.5},
            "memory": {"percent": 40.0, "used_bytes": 400, "total_bytes": 1000},
            "system": {"load_1m": 0.5},
        }
    )
    response = TestClient(app).get("/prometheus")
    assert response.status_code == 200
    assert 'agent_cpu_percent{hostname="test"} 12.5' in response.text