import pytest


@pytest.mark.django_db
def test_health_reports_database_and_sandbox(api_client):
    response = api_client.get("/api/health/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "ok"
    assert payload["terminal"]["engine"] == "bubblewrap"
