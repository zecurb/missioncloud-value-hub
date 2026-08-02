from fastapi.testclient import TestClient

from missioncloud_value_hub.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "missioncloud-value-hub-api",
    }
