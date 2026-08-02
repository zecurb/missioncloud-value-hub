from fastapi.testclient import TestClient

from missioncloud_value_hub.main import app

client = TestClient(app)


def test_value_summary_contains_decision_metrics() -> None:
    response = client.get("/api/v1/value/summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_cloud_spend"]["currency"] == "USD"
    assert payload["open_opportunities"] == 18
    assert float(payload["allocation_coverage_percent"]) >= 90


def test_opportunities_are_ranked_and_actionable() -> None:
    response = client.get("/api/v1/value/opportunities")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 4
    assert payload[0]["id"] == "opp-001"
    assert float(payload[0]["estimated_monthly_savings"]["amount"]) > 0
    assert payload[0]["owner_team"]
