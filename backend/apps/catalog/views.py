from __future__ import annotations

from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Module
from .serializers import LessonDetailSerializer


def course_queryset():
    return (
        Course.objects.filter(is_published=True)
        .annotate(
            lesson_count_annotated=Count("modules__lessons", distinct=True),
            module_count_annotated=Count("modules", distinct=True),
        )
        .prefetch_related(
            Prefetch(
                "modules",
                queryset=Module.objects.prefetch_related("lessons"),
            )
        )
    )


class LessonDetailView(APIView):
    def get(self, request, slug: str):
        lesson = get_object_or_404(
            Lesson.objects.select_related("module__course").filter(
                module__course__is_published=True
            ),
            slug=slug,
        )
        course = get_object_or_404(course_queryset(), pk=lesson.module.course_id)
        ordered_lessons = list(
            Lesson.objects.filter(module__course=course)
            .select_related("module")
            .order_by("module__position", "position", "id")
        )
        serializer = LessonDetailSerializer(
            lesson,
            context={
                "request": request,
                "course": course,
                "ordered_lessons": ordered_lessons,
            },
        )
        return Response(serializer.data)
