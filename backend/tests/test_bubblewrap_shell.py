from __future__ import annotations

import asyncio
import shutil
import subprocess

import pytest

from apps.terminal.services.bubblewrap import BubblewrapShell


def _bwrap_is_usable() -> bool:
    if shutil.which("bwrap") is None:
        return False
    result = subprocess.run(
        [
            "bwrap",
            "--ro-bind",
            "/usr",
            "/usr",
            "--ro-bind",
            "/bin",
            "/bin",
            "--ro-bind",
            "/lib",
            "/lib",
            "--ro-bind",
            "/lib64",
            "/lib64",
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--unshare-all",
            "--die-with-parent",
            "/bin/sh",
            "-c",
            "true",
        ],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


pytestmark = pytest.mark.skipif(
    not _bwrap_is_usable(),
    reason="bubblewrap or user namespaces are unavailable on this host",
)


async def _read_until_prompt(shell: BubblewrapShell, timeout: float = 5.0) -> bytes:
    output = b""
    deadline = asyncio.get_running_loop().time() + timeout
    while b"$ " not in output and asyncio.get_running_loop().time() < deadline:
        remaining = deadline - asyncio.get_running_loop().time()
        chunk = await asyncio.wait_for(shell.read(), timeout=max(0.05, remaining))
        if not chunk:
            break
        output += chunk
    return output


@pytest.mark.asyncio
async def test_sandbox_runs_commands_with_starter_files(tmp_path, settings):
    settings.TERMINAL_WORK_ROOT = tmp_path
    shell = BubblewrapShell(
        session_id="integration-test",
        files={"hello.txt": "sandbox says hi\n"},
        directories=["projects"],
    )

    await shell.start()
    try:
        welcome = await _read_until_prompt(shell)
        assert b"kernl sandbox" in welcome

        await shell.write(b"pwd\n")
        output = await _read_until_prompt(shell)
        assert b"/home/learner" in output

        await shell.write(b"cat hello.txt\n")
        output = await _read_until_prompt(shell)
        assert b"sandbox says hi" in output

        await shell.write(b"ls\n")
        output = await _read_until_prompt(shell)
        assert b"hello.txt" in output
        assert b"projects" in output
    finally:
        await shell.close()

    assert list(tmp_path.iterdir()) == []


@pytest.mark.asyncio
async def test_sandbox_has_no_network(tmp_path, settings):
    settings.TERMINAL_WORK_ROOT = tmp_path
    shell = BubblewrapShell(session_id="network-test")

    await shell.start()
    try:
        await _read_until_prompt(shell)
        await shell.write(
            b"curl -s --max-time 2 https://example.com || echo NO_NETWORK\n"
        )
        output = await _read_until_prompt(shell, timeout=7)
        assert b"NO_NETWORK" in output
    finally:
        await shell.close()
