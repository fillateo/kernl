from django.urls import path

from .views import TerminalSessionCreateView

app_name = "terminal"

urlpatterns = [
    path(
        "sessions/",
        TerminalSessionCreateView.as_view(),
        name="session-create",
    ),
]
