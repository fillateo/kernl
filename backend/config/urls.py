from django.urls import include, path

from apps.core.views import health

urlpatterns = [
    path("api/health/", health, name="health"),
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/terminal/", include("apps.terminal.urls")),
]
