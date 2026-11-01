from django.urls import path

from .views import CourseDetailView, CourseListView, LessonDetailView

app_name = "catalog"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path(
        "courses/<slug:slug>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path("lessons/<slug:slug>/", LessonDetailView.as_view(), name="lesson-detail"),
]
