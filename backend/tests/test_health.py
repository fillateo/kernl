import pytest


@pytest.mark.django_db
def test_health_reports_database_and_sandbox(api_client, monkeypatch):
    monkeypatch.setattr("apps.core.views._sandbox_available", lambda: True)

    response = api_client.get("/api/health/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "ok"
    assert payload["terminal"] == {
        "sandbox": "available",
        "engine": "bubblewrap",
    }


@pytest.mark.django_db
def test_health_degrades_when_the_nested_sandbox_is_unavailable(
    api_client, monkeypatch
):
    monkeypatch.setattr("apps.core.views._sandbox_available", lambda: False)

    response = api_client.get("/api/health/")

    # The catalog is still useful, so a broken terminal degrades rather than
    # taking the entire HTTP service down.
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["terminal"]["sandbox"] == "unavailable"
