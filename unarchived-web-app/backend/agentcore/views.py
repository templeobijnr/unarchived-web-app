

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

from . import agent

class AIChatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        user = request.user
        message = request.data.get("message")
        if not message:
            return Response({"error": "No message provided"}, status=400)

        copilot_agent = agent.create_co_pilot_agent(session_id=str(user.id), user=user)
        response = copilot_agent.run(message)
        return Response({"response": response})
