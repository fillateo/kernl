from __future__ import annotations

from django.conf import settings
from django.utils.module_loading import import_string

from .base import TerminalShell


def create_terminal_shell(
    *,
    session_id: str,
    files: dict[str, str] | None,
    directories: list[str] | None,
    executables: list[str] | None,
) -> TerminalShell:
    """Build the configured shell backend.

    The indirection keeps the WebSocket consumer independent from bubblewrap
    and lets the test suite inject a deterministic shell.
    """

    shell_class = import_string(settings.TERMINAL_SHELL_CLASS)
    return shell_class(
        session_id=session_id,
        files=files or {},
        directories=directories or [],
        executables=executables or [],
    )
