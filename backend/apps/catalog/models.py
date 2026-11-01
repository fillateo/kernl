from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    class Accent(models.TextChoices):
        LIME = "lime", "Lime"
        VIOLET = "violet", "Violet"
        CORAL = "coral", "Coral"
        SKY = "sky", "Sky"

    class Icon(models.TextChoices):
        TERMINAL = "terminal", "Terminal"
        BRANCH = "branch", "Branch"
        CODE = "code", "Code"

    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=120)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(
        max_length=20, choices=Level.choices, default=Level.BEGINNER
    )
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    accent = models.CharField(
        max_length=20, choices=Accent.choices, default=Accent.LIME
    )
    icon = models.CharField(max_length=20, choices=Icon.choices, default=Icon.TERMINAL)
    outcomes = models.JSONField(default=list, blank=True)
    tools = models.JSONField(default=list, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("position", "title")
        indexes = [models.Index(fields=("is_published", "position"))]

    def __str__(self) -> str:
        return self.title

    def count_lessons(self) -> int:
        return Lesson.objects.filter(module__course=self).count()


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    summary = models.CharField(max_length=240, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "position"), name="unique_module_position"
            )
        ]

    def __str__(self) -> str:
        return f"{self.course.title} · {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=140)
    summary = models.CharField(max_length=280)
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_mandatory = models.BooleanField(default=True)
    position = models.PositiveSmallIntegerField(default=0)
    content = models.JSONField(
        default=list,
        blank=True,
        help_text="Ordered lesson blocks rendered by the Next.js client.",
    )
    initial_files = models.JSONField(
        default=dict,
        blank=True,
        help_text="Map of relative path to file content for the sandbox.",
    )
    initial_directories = models.JSONField(default=list, blank=True)
    initial_executables = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ("position", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("module", "position"), name="unique_lesson_position"
            )
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def course(self) -> Course:
        return self.module.course
