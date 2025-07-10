
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .agent import create_co_pilot_agent

class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        message = request.data.get("message")
        if not message:
            return Response({"error": "No message provided"}, status=400)

        agent = create_co_pilot_agent(session_id=str(user.id))
        response = agent.run(message)

        return Response({"response": response})
