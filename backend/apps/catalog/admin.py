from django.contrib import admin

from .models import Course, Lesson, Module


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = (
        "position",
        "title",
        "slug",
        "duration_minutes",
        "is_mandatory",
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("position",)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ("position", "title", "summary")
    ordering = ("position",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "level",
        "position",
        "is_published",
        "duration_minutes",
    )
    list_editable = ("position", "is_published")
    list_filter = ("level", "accent", "is_published")
    search_fields = ("title", "tagline", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ModuleInline,)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position")
    list_filter = ("course",)
    search_fields = ("title", "course__title")
    inlines = (LessonInline,)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "module",
        "position",
        "duration_minutes",
        "is_mandatory",
    )
    list_filter = ("is_mandatory", "module__course")
    search_fields = ("title", "summary", "slug")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "module",
                    "title",
                    "slug",
                    "summary",
                    "duration_minutes",
                    "is_mandatory",
                    "position",
                )
            },
        ),
        ("Lesson content", {"fields": ("content",)}),
        (
            "Sandbox seed",
            {
                "fields": (
                    "initial_files",
                    "initial_directories",
                    "initial_executables",
                ),
                "description": (
                    "Files are written to /home/learner inside an isolated "
                    "bubblewrap sandbox."
                ),
            },
        ),
    )
