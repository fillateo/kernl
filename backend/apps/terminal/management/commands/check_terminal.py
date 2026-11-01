from __future__ import annotations

import asyncio
import time

from django.core.management.base import BaseCommand, CommandError

from apps.terminal.services.base import TerminalError
from apps.terminal.services.bubblewrap import BubblewrapShell

_MARKER = "KERNL_SANDBOX_OK"


class Command(BaseCommand):
    help = "Boot one real bubblewrap terminal and verify that it runs a command."

    def handle(self, *args, **options):
        try:
            output = asyncio.run(self._probe())
        except (TerminalError, OSError, TimeoutError) as exc:
            raise CommandError(f"Terminal sandbox check failed: {exc}") from exc

        if _MARKER not in output:
            raise CommandError(
                "Terminal sandbox check failed: marker not found in shell output. "
                f"Last output: {output[-500:]!r}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Terminal sandbox check passed: bash is isolated and responsive."
            )
        )

    async def _probe(self) -> str:
        shell = BubblewrapShell(
            session_id="management-check",
            files={
                "check.sh": "#!/usr/bin/env bash\nprintf 'KERNL_%s\\n' SANDBOX_OK\n"
            },
            executables=["check.sh"],
        )
        await shell.start()
        output = b""
        try:
            await shell.write(b"./check.sh\n")
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                chunk = await asyncio.wait_for(shell.read(), timeout=1)
                if not chunk:
                    break
                output += chunk
                if _MARKER.encode() in output:
                    break
        finally:
            await shell.close()
        return output.decode("utf-8", errors="replace")
