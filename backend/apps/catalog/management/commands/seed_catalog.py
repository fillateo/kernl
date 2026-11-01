from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import Course, Lesson, Module
from apps.catalog.seed_data import COURSES


class Command(BaseCommand):
    help = "Create or update the local course catalog and lesson content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Remove lessons and modules that are no longer in seed data.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        course_count = 0
        lesson_count = 0
        seen_course_slugs: set[str] = set()

        for course_position, course_data in enumerate(COURSES, start=1):
            modules = course_data["modules"]
            course, _ = Course.objects.update_or_create(
                slug=course_data["slug"],
                defaults={
                    "title": course_data["title"],
                    "tagline": course_data["tagline"],
                    "description": course_data["description"],
                    "level": course_data["level"],
                    "icon": course_data["icon"],
                    "position": course_position,
                    "is_published": True,
                },
            )
            course_count += 1
            seen_course_slugs.add(course.slug)

            seen_module_positions: set[int] = set()
            seen_lesson_slugs: set[str] = set()

            for module_position, module_data in enumerate(modules, start=1):
                module, _ = Module.objects.update_or_create(
                    course=course,
                    position=module_position,
                    defaults={
                        "title": module_data["title"],
                        "summary": module_data.get("summary", ""),
                    },
                )
                seen_module_positions.add(module_position)

                for lesson_position, lesson_data in enumerate(
                    module_data["lessons"], start=1
                ):
                    lesson, _ = Lesson.objects.update_or_create(
                        slug=lesson_data["slug"],
                        defaults={
                            "module": module,
                            "title": lesson_data["title"],
                            "summary": lesson_data["summary"],
                            "duration_minutes": lesson_data["duration_minutes"],
                            "is_mandatory": lesson_data.get("is_mandatory", True),
                            "position": lesson_position,
                            "content": lesson_data.get("content", []),
                            "initial_files": lesson_data.get("initial_files", {}),
                            "initial_directories": lesson_data.get(
                                "initial_directories", []
                            ),
                            "initial_executables": lesson_data.get(
                                "initial_executables", []
                            ),
                        },
                    )
                    seen_lesson_slugs.add(lesson.slug)
                    lesson_count += 1

            if options["prune"]:
                Module.objects.filter(course=course).exclude(
                    position__in=seen_module_positions
                ).delete()
                Lesson.objects.filter(module__course=course).exclude(
                    slug__in=seen_lesson_slugs
                ).delete()

        if options["prune"]:
            # The app exposes only one track. Remove stale courses from older
            # local databases so direct lesson URLs cannot resurrect them.
            Course.objects.exclude(slug__in=seen_course_slugs).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {course_count} courses and {lesson_count} lessons."
            )
        )
