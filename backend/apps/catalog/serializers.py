from __future__ import annotations

from rest_framework import serializers

from .models import Course, Lesson, Module


class LessonSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "slug",
            "title",
            "summary",
            "duration_minutes",
            "is_mandatory",
            "position",
        )


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ("id", "title", "summary", "position", "lessons")


class CourseListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    module_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "slug",
            "title",
            "tagline",
            "description",
            "level",
            "duration_minutes",
            "accent",
            "icon",
            "outcomes",
            "tools",
            "lesson_count",
            "module_count",
        )

    def get_lesson_count(self, obj: Course) -> int:
        annotated = getattr(obj, "lesson_count_annotated", None)
        return annotated if annotated is not None else obj.count_lessons()

    def get_module_count(self, obj: Course) -> int:
        annotated = getattr(obj, "module_count_annotated", None)
        return annotated if annotated is not None else obj.modules.count()


class CourseDetailSerializer(CourseListSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    first_lesson = serializers.SerializerMethodField()

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ("modules", "first_lesson")

    def get_first_lesson(self, obj: Course) -> str | None:
        for module in obj.modules.all():
            lessons = list(module.lessons.all())
            if lessons:
                return lessons[0].slug
        return None


class LessonDetailSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    previous_lesson = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()
    lesson_number = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "slug",
            "title",
            "summary",
            "duration_minutes",
            "is_mandatory",
            "position",
            "content",
            "course",
            "module",
            "previous_lesson",
            "next_lesson",
            "lesson_number",
            "total_lessons",
        )

    @property
    def _course(self) -> Course:
        return self.context["course"]

    @property
    def _ordered_lessons(self) -> list[Lesson]:
        return self.context["ordered_lessons"]

    def get_course(self, obj: Lesson) -> dict:
        return CourseDetailSerializer(self._course, context=self.context).data

    def get_module(self, obj: Lesson) -> dict:
        return {
            "id": obj.module_id,
            "title": obj.module.title,
            "summary": obj.module.summary,
            "position": obj.module.position,
        }

    def _neighbour(self, offset: int) -> dict | None:
        lessons = self._ordered_lessons
        try:
            index = lessons.index(self.instance)
        except ValueError:
            return None
        target = index + offset
        if target < 0 or target >= len(lessons):
            return None
        return LessonSummarySerializer(lessons[target]).data

    def get_previous_lesson(self, obj: Lesson) -> dict | None:
        return self._neighbour(-1)

    def get_next_lesson(self, obj: Lesson) -> dict | None:
        return self._neighbour(1)

    def get_lesson_number(self, obj: Lesson) -> int:
        return self._ordered_lessons.index(obj) + 1

    def get_total_lessons(self, obj: Lesson) -> int:
        return len(self._ordered_lessons)
