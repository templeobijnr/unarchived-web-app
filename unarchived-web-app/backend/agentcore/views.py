
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from . import agent

class AIChatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        messages = request.data.get("messages", [])
        result = agent.chat_session(messages)
        return Response(result)
