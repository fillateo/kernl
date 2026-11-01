from __future__ import annotations

import shutil
import time
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.terminal.models import TerminalSession

_MAX_AGE_SECONDS = 2 * 24 * 60 * 60


class Command(BaseCommand):
    help = "Remove stale terminal tickets and orphaned sandbox directories."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(seconds=_MAX_AGE_SECONDS)
        sessions = TerminalSession.objects.filter(created_at__lt=cutoff)
        count = sessions.count()
        sessions.delete()

        removed_dirs = 0
        root = Path(settings.TERMINAL_WORK_ROOT)
        if root.exists():
            oldest = time.time() - _MAX_AGE_SECONDS
            for child in root.iterdir():
                if child.is_dir() and child.stat().st_mtime < oldest:
                    shutil.rmtree(child, ignore_errors=True)
                    removed_dirs += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Removed {count} old session(s) and {removed_dirs} sandbox folder(s)."
            )
        )
