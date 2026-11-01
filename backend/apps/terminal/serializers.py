from rest_framework import serializers

from .models import TerminalSession


class TerminalSessionCreateSerializer(serializers.Serializer):
    lesson_slug = serializers.SlugField(
        required=False,
        allow_blank=True,
        max_length=100,
    )


class TerminalSessionSerializer(serializers.ModelSerializer):
    websocket_path = serializers.SerializerMethodField()

    class Meta:
        model = TerminalSession
        fields = ("id", "expires_at", "websocket_path")

    def get_websocket_path(self, obj: TerminalSession) -> str:
        return f"/ws/terminal/{obj.id}/"
