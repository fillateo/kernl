from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.catalog.models import Lesson

from .models import TerminalSession
from .serializers import (
    TerminalSessionCreateSerializer,
    TerminalSessionSerializer,
)


class TerminalSessionCreateView(APIView):
    """Issue a short-lived, single-use ticket for a WebSocket terminal."""

    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "terminal_session"

    def post(self, request):
        payload = TerminalSessionCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        now = timezone.now()
        active_count = TerminalSession.objects.filter(
            closed_at__isnull=True,
            expires_at__gt=now,
        ).count()
        if active_count >= settings.TERMINAL_MAX_SESSIONS:
            return Response(
                {
                    "detail": "All local sandboxes are busy. Try again shortly.",
                    "code": "sandbox_busy",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        lesson = None
        lesson_slug = payload.validated_data.get("lesson_slug")
        if lesson_slug:
            lesson = get_object_or_404(
                Lesson.objects.filter(module__course__is_published=True),
                slug=lesson_slug,
            )

        session = TerminalSession.objects.create(
            lesson=lesson,
            expires_at=now + timedelta(seconds=settings.TERMINAL_SESSION_TTL_SECONDS),
        )
        serializer = TerminalSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
