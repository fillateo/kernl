from __future__ import annotations

import asyncio

from apps.terminal.services.base import TerminalShell


class FakeShell(TerminalShell):
    """Deterministic in-process shell used by the WebSocket tests."""

    instances: list[FakeShell] = []

    def __init__(
        self,
        *,
        session_id: str,
        files: dict[str, str] | None = None,
        directories: list[str] | None = None,
        executables: list[str] | None = None,
    ) -> None:
        self.session_id = session_id
        self.files = files or {}
        self.directories = directories or []
        self.executables = executables or []
        self.outgoing: asyncio.Queue[bytes] = asyncio.Queue()
        self.started = False
        self.closed = False
        self.last_resize: tuple[int, int] | None = None
        FakeShell.instances.append(self)

    async def start(self) -> None:
        self.started = True
        await self.outgoing.put(b"fake shell ready\r\n")

    async def read(self) -> bytes:
        return await self.outgoing.get()

    async def write(self, data: bytes) -> None:
        await self.outgoing.put(b"echo:" + data)

    async def resize(self, cols: int, rows: int) -> None:
        self.last_resize = (cols, rows)

    async def close(self) -> None:
        self.closed = True
        await self.outgoing.put(b"")
