from django.contrib import admin

from .models import TerminalSession


@admin.register(TerminalSession)
class TerminalSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lesson",
        "created_at",
        "connected_at",
        "closed_at",
        "close_reason",
    )
    list_filter = ("close_reason", "created_at")
    search_fields = ("id", "lesson__title")
    readonly_fields = (
        "id",
        "created_at",
        "connected_at",
        "closed_at",
        "close_reason",
    )
    date_hierarchy = "created_at"
