from django.urls import path

from .views import LessonDetailView

app_name = "catalog"

urlpatterns = [
    path("lessons/<slug:slug>/", LessonDetailView.as_view(), name="lesson-detail"),
]
