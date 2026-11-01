from __future__ import annotations

import asyncio
from datetime import timedelta

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.utils import timezone

from apps.terminal.models import TerminalSession
from apps.terminal.tests.fakes import FakeShell
from config.asgi import application


def _create_session(**kwargs) -> TerminalSession:
    return TerminalSession.objects.create(**kwargs)


@pytest.fixture(autouse=True)
def fake_shell(settings):
    FakeShell.instances.clear()
    settings.TERMINAL_SHELL_CLASS = "apps.terminal.tests.fakes.FakeShell"
    settings.TERMINAL_MAX_OUTPUT_BYTES = 2 * 1024 * 1024
    yield
    FakeShell.instances.clear()


def _communicator(session_id, origin: str = "http://localhost:3000"):
    return WebsocketCommunicator(
        application,
        f"/ws/terminal/{session_id}/",
        headers=[(b"origin", origin.encode())],
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_bridges_input_output_and_resize():
    session = await database_sync_to_async(_create_session)(
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    communicator = _communicator(session.id)

    connected, _ = await communicator.connect()
    assert connected

    ready = await communicator.receive_json_from(timeout=2)
    assert ready["type"] == "ready"
    assert ready["cwd"] == "/home/learner"

    boot = await communicator.receive_json_from(timeout=2)
    assert boot["type"] == "output"
    assert "fake shell ready" in boot["data"]

    await communicator.send_json_to({"type": "input", "data": "ls\n"})
    echoed = await communicator.receive_json_from(timeout=2)
    assert echoed == {"type": "output", "data": "echo:ls\n"}

    await communicator.send_json_to({"type": "resize", "cols": 100, "rows": 30})
    await asyncio.sleep(0.05)
    assert FakeShell.instances[0].last_resize == (100, 30)

    await communicator.send_json_to({"type": "ping"})
    assert await communicator.receive_json_from(timeout=2) == {"type": "pong"}

    await communicator.disconnect()

    await database_sync_to_async(session.refresh_from_db)()
    assert session.connected_at is not None
    assert session.closed_at is not None
    assert session.close_reason == "client_disconnect"
    assert FakeShell.instances[0].closed is True


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_rejects_a_consumed_ticket():
    session = await database_sync_to_async(_create_session)(
        expires_at=timezone.now() + timedelta(minutes=10),
        connected_at=timezone.now(),
    )
    communicator = _communicator(session.id)

    connected, _ = await communicator.connect()

    assert connected is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_rejects_an_expired_ticket():
    session = await database_sync_to_async(_create_session)(
        expires_at=timezone.now() - timedelta(seconds=1),
    )
    communicator = _communicator(session.id)

    connected, _ = await communicator.connect()

    assert connected is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_rejects_an_untrusted_origin(terminal_session):
    communicator = _communicator(
        terminal_session.id,
        origin="http://evil.example",
    )

    connected, _ = await communicator.connect()

    assert connected is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_invalid_messages_return_errors_without_closing(terminal_session):
    communicator = _communicator(terminal_session.id)
    await communicator.connect()
    await communicator.receive_json_from(timeout=2)
    await communicator.receive_json_from(timeout=2)

    await communicator.send_json_to({"type": "input", "data": 123})
    error = await communicator.receive_json_from(timeout=2)
    assert error["type"] == "error"
    assert error["code"] == "bad_input"

    await communicator.send_json_to({"type": "resize", "cols": 0, "rows": 30})
    error = await communicator.receive_json_from(timeout=2)
    assert error["code"] == "bad_resize"

    await communicator.send_json_to({"type": "not-a-thing"})
    error = await communicator.receive_json_from(timeout=2)
    assert error["code"] == "bad_message"

    await communicator.send_json_to({"type": "ping"})
    assert await communicator.receive_json_from(timeout=2) == {"type": "pong"}

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_output_limit_closes_the_socket(settings):
    settings.TERMINAL_MAX_OUTPUT_BYTES = 8
    session = await database_sync_to_async(_create_session)(
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    communicator = _communicator(session.id)
    await communicator.connect()

    assert (await communicator.receive_json_from(timeout=2))["type"] == "ready"
    error = await communicator.receive_json_from(timeout=2)
    assert error["code"] == "output_limit"

    close_event = await communicator.receive_output(timeout=2)
    assert close_event["type"] == "websocket.close"
    assert close_event["code"] == 1008

    await communicator.disconnect()
    await asyncio.sleep(0.1)
    await database_sync_to_async(session.refresh_from_db)()
    assert session.closed_at is not None
    assert session.close_reason == "output_limit"


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_idle_timeout_closes_the_socket(settings):
    settings.TERMINAL_IDLE_TIMEOUT_SECONDS = 0.1
    settings.TERMINAL_MAX_LIFETIME_SECONDS = 30
    session = await database_sync_to_async(_create_session)(
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    communicator = _communicator(session.id)
    await communicator.connect()

    assert (await communicator.receive_json_from(timeout=2))["type"] == "ready"
    assert (await communicator.receive_json_from(timeout=2))["type"] == "output"
    error = await communicator.receive_json_from(timeout=3)
    assert error["code"] == "idle_timeout"

    close_event = await communicator.receive_output(timeout=2)
    assert close_event["type"] == "websocket.close"
    assert close_event["code"] == 4001

    await communicator.disconnect()
    await asyncio.sleep(0.1)
    await database_sync_to_async(session.refresh_from_db)()
    assert session.closed_at is not None
    assert session.close_reason == "idle_timeout"
