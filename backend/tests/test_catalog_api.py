from __future__ import annotations

import pytest
from django.core.management import call_command

from apps.catalog.models import Course


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
def test_unpublished_course_is_not_served(api_client, course):
    course.is_published = False
    course.save(update_fields=["is_published"])

    response = api_client.get("/api/v1/catalog/lessons/test-lesson/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_seed_command_is_idempotent():
    call_command("seed_catalog")
    call_command("seed_catalog")

    assert Course.objects.count() == 1
    assert Course.objects.get(slug="git-essentials").modules.count() == 2
