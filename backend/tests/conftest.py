from __future__ import annotations

from datetime import timedelta

import pytest
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APIClient

from apps.catalog.models import Course, Lesson, Module
from apps.terminal.models import TerminalSession


@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient(HTTP_HOST="localhost")


@pytest.fixture
def course(db) -> Course:
    course = Course.objects.create(
        slug="test-course",
        title="Test Course",
        tagline="A compact test track.",
        description="A course created for the test suite.",
        level=Course.Level.BEGINNER,
        icon=Course.Icon.TERMINAL,
        position=1,
    )
    module = Module.objects.create(
        course=course,
        title="Test module",
        summary="The first module.",
        position=1,
    )
    Lesson.objects.create(
        module=module,
        slug="test-lesson",
        title="Test Lesson",
        summary="A test lesson.",
        duration_minutes=10,
        position=1,
        content=[{"type": "paragraph", "text": "Hello"}],
    )
    Lesson.objects.create(
        module=module,
        slug="test-lesson-two",
        title="Second Test Lesson",
        summary="Another test lesson.",
        duration_minutes=12,
        position=2,
        content=[],
    )
    return course


@pytest.fixture
def terminal_session(db) -> TerminalSession:
    return TerminalSession.objects.create(
        expires_at=timezone.now() + timedelta(minutes=10)
    )
