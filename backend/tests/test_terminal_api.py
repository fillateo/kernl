from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.terminal.models import TerminalSession


@pytest.mark.django_db
def test_create_terminal_session(api_client, course):
    response = api_client.post(
        "/api/v1/terminal/sessions/",
        {"lesson_slug": "test-lesson"},
        format="json",
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["websocket_path"] == f"/ws/terminal/{payload['id']}/"
    session = TerminalSession.objects.get(pk=payload["id"])
    assert session.lesson.slug == "test-lesson"
    assert session.connected_at is None


@pytest.mark.django_db
def test_create_terminal_session_without_lesson(api_client):
    response = api_client.post(
        "/api/v1/terminal/sessions/",
        {},
        format="json",
    )

    assert response.status_code == 201
    assert TerminalSession.objects.get(pk=response.json()["id"]).lesson is None


@pytest.mark.django_db
def test_unknown_lesson_is_rejected(api_client):
    response = api_client.post(
        "/api/v1/terminal/sessions/",
        {"lesson_slug": "missing"},
        format="json",
    )

    assert response.status_code == 404
    assert TerminalSession.objects.count() == 0


@pytest.mark.django_db
def test_session_limit_returns_503(api_client, settings):
    settings.TERMINAL_MAX_SESSIONS = 1
    TerminalSession.objects.create(expires_at=timezone.now() + timedelta(minutes=10))

    response = api_client.post(
        "/api/v1/terminal/sessions/",
        {},
        format="json",
    )

    assert response.status_code == 503
    assert response.json()["code"] == "sandbox_busy"


@pytest.mark.django_db
def test_cors_preflight_allows_the_frontend_origin(api_client):
    response = api_client.options(
        "/api/v1/terminal/sessions/",
        HTTP_ORIGIN="http://localhost:3000",
        HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        HTTP_ACCESS_CONTROL_REQUEST_HEADERS="content-type",
    )

    assert response.status_code == 200
    assert response["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in response["access-control-allow-methods"]
