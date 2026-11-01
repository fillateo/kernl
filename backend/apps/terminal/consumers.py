from __future__ import annotations

import asyncio
import codecs
import logging
import time
from contextlib import suppress

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import TerminalSession
from .services.base import TerminalError, TerminalUnavailable
from .services.factory import create_terminal_shell

logger = logging.getLogger(__name__)

_MAX_INPUT_BYTES = 16 * 1024
_MAX_RESIZE_COLS = 400
_MAX_RESIZE_ROWS = 200


class TerminalConsumer(AsyncJsonWebsocketConsumer):
    """Bridges the browser's xterm.js instance to one isolated PTY.

    Protocol (JSON both ways):
      client -> {"type":"input","data":"ls\\r"}
      client -> {"type":"resize","cols":120,"rows":32}
      client -> {"type":"ping"}
      server -> {"type":"ready","cwd":"/home/learner"}
      server -> {"type":"output","data":"..."}
      server -> {"type":"pong"}
      server -> {"type":"error","code":"...","message":"..."}
      server -> {"type":"exit","code":0}
    """

    async def connect(self) -> None:
        self._shell = None
        self._reader_task: asyncio.Task | None = None
        self._watchdog_task: asyncio.Task | None = None
        self._cleaned = False
        self._session_id: str | None = None
        self._close_reason = "client_disconnect"
        self._output_bytes = 0
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self._started_at = time.monotonic()
        self._last_activity = self._started_at

        session_id = self.scope["url_route"]["kwargs"]["session_id"]
        session = await self._claim_session(session_id)
        if session is None:
            # Reject the handshake: missing, expired, or already-consumed.
            await self.close(code=4404)
            return

        self._session_id = session["id"]
        await self.accept()

        try:
            shell = create_terminal_shell(
                session_id=self._session_id,
                files=session["files"],
                directories=session["directories"],
                executables=session["executables"],
            )
            await shell.start()
        except TerminalUnavailable as exc:
            logger.warning("Terminal backend unavailable: %s", exc)
            self._close_reason = "sandbox_unavailable"
            await self._send_error(
                "The local sandbox could not start. Check that bubblewrap is "
                "installed and user namespaces are enabled, then restart the server.",
                code="sandbox_unavailable",
            )
            await self.close(code=1011)
            return
        except (TerminalError, OSError):
            logger.exception("Unable to start terminal session %s", self._session_id)
            self._close_reason = "sandbox_error"
            await self._send_error(
                "The sandbox could not start. Please open a new session.",
                code="sandbox_error",
            )
            await self.close(code=1011)
            return

        if self._cleaned:
            await shell.close()
            return
        self._shell = shell
        try:
            await self.send_json(
                {
                    "type": "ready",
                    "cwd": "/home/learner",
                    "sessionId": self._session_id,
                }
            )
        except Exception:
            await self._cleanup()
            return
        if self._cleaned:
            return
        self._reader_task = asyncio.create_task(self._pump_output())
        self._watchdog_task = asyncio.create_task(self._watchdog())

    async def disconnect(self, close_code: int) -> None:
        await self._cleanup()

    async def receive_json(self, content, **kwargs) -> None:
        if not isinstance(content, dict):
            await self._send_error("Expected a JSON object.", code="bad_message")
            return

        message_type = content.get("type")
        if message_type == "input":
            await self._handle_input(content)
        elif message_type == "resize":
            await self._handle_resize(content)
        elif message_type == "ping":
            await self.send_json({"type": "pong"})
        else:
            await self._send_error(
                f"Unsupported message type: {message_type!r}",
                code="bad_message",
            )

    async def _handle_input(self, content: dict) -> None:
        data = content.get("data")
        if not isinstance(data, str):
            await self._send_error("Input must be a string.", code="bad_input")
            return
        encoded = data.encode("utf-8")
        if len(encoded) > _MAX_INPUT_BYTES:
            await self._send_error("Input is too large.", code="input_too_large")
            return
        if self._shell is None:
            await self._send_error("Terminal is not ready.", code="not_ready")
            return
        self._last_activity = time.monotonic()
        try:
            await self._shell.write(encoded)
        except TerminalError:
            await self._send_error("Terminal input failed.", code="input_failed")

    async def _handle_resize(self, content: dict) -> None:
        cols = content.get("cols")
        rows = content.get("rows")
        if (
            not isinstance(cols, int)
            or isinstance(cols, bool)
            or not isinstance(rows, int)
            or isinstance(rows, bool)
            or cols < 1
            or rows < 1
            or cols > _MAX_RESIZE_COLS
            or rows > _MAX_RESIZE_ROWS
        ):
            await self._send_error("Invalid terminal size.", code="bad_resize")
            return
        if self._shell is None:
            return
        try:
            await self._shell.resize(cols, rows)
        except TerminalError:
            logger.debug("Resize failed for session %s", self._session_id)

    async def _pump_output(self) -> None:
        assert self._shell is not None
        try:
            while True:
                data = await self._shell.read()
                if not data:
                    tail = self._decoder.decode(b"", final=True)
                    if tail:
                        await self.send_json({"type": "output", "data": tail})
                    self._close_reason = "shell_exit"
                    await self.send_json({"type": "exit", "code": 0})
                    await self.close(code=1000)
                    return

                self._output_bytes += len(data)
                if self._output_bytes > settings.TERMINAL_MAX_OUTPUT_BYTES:
                    self._close_reason = "output_limit"
                    await self._send_error(
                        "Output limit reached. Restart the terminal to continue.",
                        code="output_limit",
                    )
                    await self.close(code=1008)
                    return

                text = self._decoder.decode(data)
                if text:
                    await self.send_json({"type": "output", "data": text})
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Terminal read failed for session %s", self._session_id)
            self._close_reason = "read_error"
            await self._send_error(
                "The terminal connection was interrupted.",
                code="read_error",
            )
            await self.close(code=1011)

    async def _watchdog(self) -> None:
        interval = max(
            1,
            min(
                30,
                settings.TERMINAL_IDLE_TIMEOUT_SECONDS // 2,
                settings.TERMINAL_MAX_LIFETIME_SECONDS // 2,
            ),
        )
        try:
            while True:
                await asyncio.sleep(interval)
                now = time.monotonic()
                if now - self._last_activity > settings.TERMINAL_IDLE_TIMEOUT_SECONDS:
                    self._close_reason = "idle_timeout"
                    await self._send_error(
                        "Session closed after a period of inactivity.",
                        code="idle_timeout",
                    )
                    await self.close(code=4001)
                    return
                if now - self._started_at > settings.TERMINAL_MAX_LIFETIME_SECONDS:
                    self._close_reason = "max_lifetime"
                    await self._send_error(
                        "Session reached its maximum lifetime. Start a new one.",
                        code="max_lifetime",
                    )
                    await self.close(code=4002)
                    return
        except asyncio.CancelledError:
            raise

    async def _send_error(self, message: str, *, code: str) -> None:
        with suppress(Exception):  # socket already closed
            await self.send_json({"type": "error", "code": code, "message": message})

    async def _cleanup(self) -> None:
        if self._cleaned:
            return
        self._cleaned = True

        current = asyncio.current_task()
        tasks = [
            task
            for task in (self._reader_task, self._watchdog_task)
            if task is not None
        ]
        for task in tasks:
            if task is not current:
                task.cancel()
        await asyncio.gather(
            *(task for task in tasks if task is not current),
            return_exceptions=True,
        )

        if self._shell is not None:
            try:
                await self._shell.close()
            except Exception:  # pragma: no cover - best effort cleanup
                logger.exception("Failed to close sandbox %s", self._session_id)
            self._shell = None

        if self._session_id is not None:
            await self._finish_session(self._close_reason)

    @database_sync_to_async
    def _claim_session(self, session_id: str) -> dict | None:
        now = timezone.now()
        try:
            with transaction.atomic():
                session = (
                    TerminalSession.objects.select_for_update()
                    .select_related("lesson")
                    .get(pk=session_id)
                )
                if (
                    session.connected_at is not None
                    or session.closed_at is not None
                    or session.expires_at <= now
                ):
                    return None
                lesson = session.lesson
                session.connected_at = now
                session.save(update_fields=["connected_at"])
                return {
                    "id": str(session.id),
                    "files": (lesson.initial_files if lesson else {}) or {},
                    "directories": (lesson.initial_directories if lesson else []) or [],
                    "executables": (lesson.initial_executables if lesson else []) or [],
                }
        except (TerminalSession.DoesNotExist, ValidationError, ValueError):
            return None

    @database_sync_to_async
    def _finish_session(self, reason: str) -> None:
        try:
            session = TerminalSession.objects.get(pk=self._session_id)
        except (TerminalSession.DoesNotExist, ValidationError, ValueError):
            return
        if session.closed_at is None:
            session.closed_at = timezone.now()
            session.close_reason = reason[:64]
            session.save(update_fields=["closed_at", "close_reason"])
