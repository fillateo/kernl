"""Run an interactive bash shell inside a bubblewrap sandbox.

The shell gets a private PID, network, IPC, UTS, cgroup, and user namespace.
Only a small, read-only slice of the host filesystem is mounted. The learner
gets one writable directory, mounted at /home/learner, which is deleted when
the WebSocket closes. There is no host home directory, Docker socket, or
network access inside the sandbox.
"""

from __future__ import annotations

import asyncio
import fcntl
import logging
import os
import pty
import resource
import shutil
import struct
import subprocess
import tempfile
import termios
from contextlib import suppress
from pathlib import Path, PurePosixPath

from django.conf import settings

from .base import TerminalError, TerminalShell, TerminalUnavailable

logger = logging.getLogger(__name__)

_MAX_FILE_BYTES = 256 * 1024
_READ_CHUNK = 64 * 1024


class BubblewrapShell(TerminalShell):
    def __init__(
        self,
        *,
        session_id: str,
        files: dict[str, str] | None = None,
        directories: list[str] | None = None,
        executables: list[str] | None = None,
        cols: int = 120,
        rows: int = 32,
    ) -> None:
        if shutil.which("bwrap") is None:
            raise TerminalUnavailable(
                "bubblewrap (bwrap) is required for the interactive terminal"
            )

        self.session_id = session_id
        self.files = files or {}
        self.directories = directories or []
        self.executables = executables or []
        self.cols = cols
        self.rows = rows

        self._root: Path | None = None
        self._home: Path | None = None
        self._master_fd: int | None = None
        self._proc: subprocess.Popen[bytes] | None = None
        self._closed = False

    # -- lifecycle -----------------------------------------------------------

    async def start(self) -> None:
        await asyncio.to_thread(self._prepare_filesystem)
        await asyncio.to_thread(self._spawn)
        # Catch the common case where bwrap itself starts but exits because
        # user namespaces are disabled. Without this check the client would see
        # a connected-but-empty terminal.
        await asyncio.sleep(0.05)
        if self._proc is not None and self._proc.poll() is not None:
            await self.close()
            raise TerminalUnavailable(
                "The sandbox exited during startup. Check that bubblewrap is "
                "installed and unprivileged user namespaces are enabled."
            )

    def _prepare_filesystem(self) -> None:
        work_root = Path(settings.TERMINAL_WORK_ROOT)
        work_root.mkdir(parents=True, exist_ok=True)
        work_root.chmod(0o700)

        self._root = Path(
            tempfile.mkdtemp(prefix=f"kernl-{self.session_id[:8]}-", dir=work_root)
        )
        self._root.chmod(0o700)
        self._home = self._root / "home"
        self._home.mkdir(mode=0o755)

        for directory in self.directories:
            target = _safe_join(self._home, directory)
            target.mkdir(parents=True, exist_ok=True, mode=0o755)

        for relative, content in self.files.items():
            if not isinstance(content, str):
                raise TerminalError("Initial file content must be text")
            encoded = content.encode("utf-8")
            if len(encoded) > _MAX_FILE_BYTES:
                raise TerminalError("Initial file is too large")
            target = _safe_join(self._home, relative)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
            target.write_text(content, encoding="utf-8")

        for relative in self.executables:
            target = _safe_join(self._home, relative)
            if target.exists():
                target.chmod(0o755)

        # Runtime files live outside the bind mount so the learner never sees
        # how the sandbox itself is wired up.
        uid = os.getuid()
        gid = os.getgid()
        (self._root / "passwd").write_text(
            f"learner:x:{uid}:{gid}:Kernl Learner:/home/learner:/bin/bash\n",
            encoding="utf-8",
        )
        (self._root / "group").write_text(
            f"learner:x:{gid}:\nnogroup:x:65534:\n", encoding="utf-8"
        )
        (self._root / "bashrc").write_text(_BASHRC, encoding="utf-8")

    def _spawn(self) -> None:
        if self._root is None or self._home is None:
            raise TerminalError("Sandbox was not prepared")

        args = self._bubblewrap_args()
        master_fd, slave_fd = pty.openpty()
        _set_winsize(slave_fd, self.cols, self.rows)

        def child_setup() -> None:
            os.setsid()
            fcntl.ioctl(slave_fd, termios.TIOCSCTTY, 0)
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(
                resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024)
            )
            resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))

        try:
            proc = subprocess.Popen(
                args,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True,
                pass_fds=(slave_fd,),
                preexec_fn=child_setup,
                env={},
            )
        except OSError as exc:  # pragma: no cover - host configuration issue
            os.close(master_fd)
            os.close(slave_fd)
            raise TerminalError("Unable to start the sandbox") from exc
        finally:
            with suppress(OSError):
                os.close(slave_fd)

        os.set_blocking(master_fd, False)
        self._master_fd = master_fd
        self._proc = proc

    def _bubblewrap_args(self) -> list[str]:
        assert self._root is not None
        assert self._home is not None

        args = [
            "bwrap",
            "--die-with-parent",
            "--unshare-all",
            "--clearenv",
            "--hostname",
            "kernl-sandbox",
            "--cap-drop",
            "ALL",
            # Read-only runtime. Nothing writes to the host system.
            "--ro-bind",
            "/usr",
            "/usr",
            "--ro-bind-try",
            "/bin",
            "/bin",
            "--ro-bind-try",
            "/sbin",
            "/sbin",
            "--ro-bind-try",
            "/lib",
            "/lib",
            "--ro-bind-try",
            "/lib64",
            "/lib64",
            "--ro-bind-try",
            "/etc/alternatives",
            "/etc/alternatives",
            "--ro-bind-try",
            "/etc/ld.so.cache",
            "/etc/ld.so.cache",
            "--ro-bind-try",
            "/etc/ld.so.conf",
            "/etc/ld.so.conf",
            "--ro-bind-try",
            "/etc/ld.so.conf.d",
            "/etc/ld.so.conf.d",
            "--ro-bind-try",
            "/etc/nsswitch.conf",
            "/etc/nsswitch.conf",
            "--ro-bind",
            str(self._root / "passwd"),
            "/etc/passwd",
            "--ro-bind",
            str(self._root / "group"),
            "/etc/group",
            "--ro-bind",
            str(self._root / "bashrc"),
            "/etc/kernl.bashrc",
            # Fresh writable surfaces.
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--tmpfs",
            "/tmp",
            "--tmpfs",
            "/run",
            "--bind",
            str(self._home),
            "/home/learner",
            "--chdir",
            "/home/learner",
            "--setenv",
            "HOME",
            "/home/learner",
            "--setenv",
            "PATH",
            "/usr/local/bin:/usr/bin:/bin",
            "--setenv",
            "TERM",
            "xterm-256color",
            "--setenv",
            "COLORTERM",
            "truecolor",
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "SHELL",
            "/bin/bash",
            "--setenv",
            "HISTFILE",
            "/dev/null",
            "--setenv",
            "LESS",
            "-FRX",
            "--setenv",
            "PAGER",
            "cat",
            "--setenv",
            "TZ",
            "UTC",
            # Git can be used in the sandbox without an interactive config
            # step. The identity is intentionally generic and local only.
            "--setenv",
            "GIT_AUTHOR_NAME",
            "Kernl Learner",
            "--setenv",
            "GIT_AUTHOR_EMAIL",
            "learner@kernl.local",
            "--setenv",
            "GIT_COMMITTER_NAME",
            "Kernl Learner",
            "--setenv",
            "GIT_COMMITTER_EMAIL",
            "learner@kernl.local",
            "--setenv",
            "GIT_CONFIG_NOSYSTEM",
            "1",
            "--setenv",
            "GIT_PAGER",
            "cat",
            "--setenv",
            "GIT_CONFIG_COUNT",
            "1",
            "--setenv",
            "GIT_CONFIG_KEY_0",
            "init.defaultBranch",
            "--setenv",
            "GIT_CONFIG_VALUE_0",
            "main",
            "/bin/bash",
            "--noprofile",
            "--rcfile",
            "/etc/kernl.bashrc",
            "-i",
        ]
        return args

    # -- I/O -----------------------------------------------------------------

    async def read(self) -> bytes:
        if self._master_fd is None or self._closed:
            return b""

        loop = asyncio.get_running_loop()
        future: asyncio.Future[bytes] = loop.create_future()
        fd = self._master_fd

        def on_readable() -> None:
            loop.remove_reader(fd)
            if future.done():
                return
            try:
                data = os.read(fd, _READ_CHUNK)
            except BlockingIOError:
                loop.add_reader(fd, on_readable)
                return
            except OSError:
                data = b""
            if not future.done():
                future.set_result(data)

        loop.add_reader(fd, on_readable)
        try:
            return await future
        finally:
            loop.remove_reader(fd)

    async def write(self, data: bytes) -> None:
        if self._master_fd is None or self._closed:
            return
        view = memoryview(data)
        while view:
            try:
                written = os.write(self._master_fd, view)
            except BlockingIOError:
                await asyncio.sleep(0.005)
                continue
            except OSError as exc:
                raise TerminalError("Terminal input failed") from exc
            view = view[written:]

    async def resize(self, cols: int, rows: int) -> None:
        if self._master_fd is None or self._closed:
            return
        try:
            _set_winsize(self._master_fd, cols, rows)
        except OSError:
            logger.debug("Unable to resize terminal %s", self.session_id)

    # -- shutdown ------------------------------------------------------------

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        await asyncio.to_thread(self._terminate_process)
        await asyncio.to_thread(self._cleanup)
        self._closed = True

    def _terminate_process(self) -> None:
        proc = self._proc
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, 15)
                proc.wait(timeout=1.5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                with suppress(ProcessLookupError):
                    os.killpg(proc.pid, 9)
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:  # pragma: no cover
                    logger.warning("Sandbox %s did not exit", self.session_id)
        if self._master_fd is not None:
            with suppress(OSError):
                os.close(self._master_fd)
            self._master_fd = None

    def _cleanup(self) -> None:
        if self._root is not None:
            shutil.rmtree(self._root, ignore_errors=True)
            self._root = None


def _safe_join(base: Path, relative: str) -> Path:
    base = base.resolve()
    if not relative or not isinstance(relative, str):
        raise TerminalError("Invalid sandbox path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise TerminalError("Sandbox paths must be relative")
    target = (base / pure).resolve()
    if target != base and base not in target.parents:
        raise TerminalError("Sandbox path escapes the workspace")
    return target


def _set_winsize(fd: int, cols: int, rows: int) -> None:
    cols = max(20, min(int(cols), 400))
    rows = max(5, min(int(rows), 200))
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))


_BASHRC = r"""
export PS1='\[\e[38;5;114m\]learner\[\e[0m\]:\[\e[38;5;111m\]\w\[\e[0m\]$ '
export HISTFILE=/dev/null
export HISTSIZE=0
export BASH_SILENCE_DEPRECATION_WARNING=1
export GIT_TERMINAL_PROMPT=0
cd /home/learner
printf '\n\033[38;5;114m  kernl sandbox\033[0m  \033[38;5;250mephemeral · no network\033[0m\n'
printf '\033[38;5;250m  Try ls, pwd, or help. Everything resets when you disconnect.\033[0m\n\n'
""".strip()
