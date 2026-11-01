"""Small operational endpoints used by local tooling and CI."""

from __future__ import annotations

import shutil
import subprocess
from functools import lru_cache

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET

_BWRAP_PROBE = [
    "bwrap",
    "--unshare-all",
    "--die-with-parent",
    "--ro-bind",
    "/usr",
    "/usr",
    "--ro-bind-try",
    "/bin",
    "/bin",
    "--ro-bind-try",
    "/lib",
    "/lib",
    "--ro-bind-try",
    "/lib64",
    "/lib64",
    "--proc",
    "/proc",
    "--dev",
    "/dev",
    "--tmpfs",
    "/tmp",
    "/bin/sh",
    "-c",
    "true",
]


@lru_cache(maxsize=1)
def _sandbox_available() -> bool:
    """Verify that bubblewrap can actually create a namespace.

    Merely finding the binary is not enough: Docker's default seccomp/AppArmor
    profiles, or a host with unprivileged user namespaces disabled, can still
    block every sandbox. The probe is cached so healthchecks stay cheap.
    """

    if shutil.which("bwrap") is None:
        return False

    try:
        result = subprocess.run(
            _BWRAP_PROBE,
            timeout=3,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


@require_GET
def health(request):
    database_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:  # pragma: no cover - only hit when the DB is unavailable
        database_ok = False

    sandbox_available = _sandbox_available()
    healthy = database_ok and sandbox_available
    return JsonResponse(
        {
            "status": "ok" if healthy else "degraded",
            "database": "ok" if database_ok else "unavailable",
            "terminal": {
                "sandbox": "available" if sandbox_available else "unavailable",
                "engine": "bubblewrap",
            },
        },
        status=200 if database_ok else 503,
    )
