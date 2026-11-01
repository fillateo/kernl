from __future__ import annotations

from abc import ABC, abstractmethod


class TerminalError(RuntimeError):
    """Base error for terminal lifecycle failures."""


class TerminalUnavailable(TerminalError):
    """Raised when the host cannot provide an isolated terminal."""


class TerminalShell(ABC):
    """Async interface shared by the real sandbox and test doubles."""

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def read(self) -> bytes: ...

    @abstractmethod
    async def write(self, data: bytes) -> None: ...

    @abstractmethod
    async def resize(self, cols: int, rows: int) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
