from django.urls import path

from .consumers import TerminalConsumer

websocket_urlpatterns = [
    path("ws/terminal/<uuid:session_id>/", TerminalConsumer.as_asgi()),
]
