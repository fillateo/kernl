"""Small operational endpoints used by local tooling and CI."""

from __future__ import annotations

import shutil

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    database_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:  # pragma: no cover - only hit when the DB is unavailable
        database_ok = False

    sandbox_available = shutil.which("bwrap") is not None
    status = "ok" if database_ok else "degraded"
    return JsonResponse(
        {
            "status": status,
            "database": "ok" if database_ok else "unavailable",
            "terminal": {
                "sandbox": "available" if sandbox_available else "unavailable",
                "engine": "bubblewrap",
            },
        },
        status=200 if database_ok else 503,
    )
