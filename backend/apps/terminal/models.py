from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class TerminalSession(models.Model):
    """A single-use ticket that authorises one WebSocket terminal.

    The ticket is created over HTTP, expires quickly, and can only be claimed
    once. It deliberately stores no command history or output.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        "catalog.Lesson",
        related_name="terminal_sessions",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    connected_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    close_reason = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("expires_at",)),
            models.Index(fields=("connected_at", "closed_at")),
        ]

    def __str__(self) -> str:
        return f"Terminal {self.pk}"

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= timezone.now()
