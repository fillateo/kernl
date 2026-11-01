from __future__ import annotations

import pytest
from django.core.management import call_command

from apps.catalog.models import Course


@pytest.mark.django_db
def test_course_list_only_returns_published_courses(api_client, course):
    Course.objects.create(
        slug="hidden-course",
        title="Hidden",
        tagline="Not published.",
        description="Hidden course.",
        level=Course.Level.BEGINNER,
        duration_minutes=20,
        accent=Course.Accent.CORAL,
        icon=Course.Icon.CODE,
        position=2,
        is_published=False,
    )

    response = api_client.get("/api/v1/catalog/courses/")

    assert response.status_code == 200
    payload = response.json()
    assert [item["slug"] for item in payload] == ["test-course"]
    assert payload[0]["lesson_count"] == 2
    assert payload[0]["module_count"] == 1


@pytest.mark.django_db
def test_course_detail_contains_modules_and_first_lesson(api_client, course):
    response = api_client.get("/api/v1/catalog/courses/test-course/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Test Course"
    assert payload["first_lesson"] == "test-lesson"
    assert payload["modules"][0]["lessons"][0]["title"] == "Test Lesson"


@pytest.mark.django_db
def test_lesson_detail_contains_navigation_and_course_outline(api_client, course):
    response = api_client.get("/api/v1/catalog/lessons/test-lesson/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_number"] == 1
    assert payload["total_lessons"] == 2
    assert payload["next_lesson"]["slug"] == "test-lesson-two"
    assert payload["previous_lesson"] is None
    assert payload["course"]["slug"] == "test-course"
    assert payload["module"]["title"] == "Test module"


@pytest.mark.django_db
def test_unknown_course_returns_404(api_client):
    response = api_client.get("/api/v1/catalog/courses/does-not-exist/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_unpublished_course_is_not_served(api_client, course):
    course.is_published = False
    course.save(update_fields=["is_published"])

    response = api_client.get("/api/v1/catalog/courses/test-course/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_seed_command_is_idempotent():
    call_command("seed_catalog")
    call_command("seed_catalog")

    assert Course.objects.count() == 3
    assert Course.objects.get(slug="linux-foundations").modules.count() == 2
