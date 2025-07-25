# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied
import logging
from agentcore.agent import ConversationalAgent
logger = logging.getLogger(__name__)
from rest_framework.decorators import action
from chat.models import Message, Conversation
from chat.serializers import MessageSerializer, ConversationSerializer

class MessagePagination(PageNumberPagination):
    page_size = 20

class MessageViewSet(viewsets.ModelViewSet):
    """Chat message management"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        """Filter messages by user and optionally by conversation"""
        qs = Message.objects.filter(user=self.request.user)
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            qs = qs.filter(conversation_id=conversation_id)
        return qs

    def perform_create(self, serializer):
        # Only allow user to create messages for themselves
        serializer.save(user=self.request.user)
        logger.info(f"Message created by user {self.request.user.id}")

    def perform_update(self, serializer):
        # Only allow user to update their own messages
        if serializer.instance.user != self.request.user:
            logger.warning(f"User {self.request.user.id} tried to update another user's message")
            raise PermissionDenied("You cannot edit this message.")
        serializer.save()
        logger.info(f"Message updated by user {self.request.user.id}")

    def perform_destroy(self, instance):
        # Only allow user to delete their own messages
        if instance.user != self.request.user:
            logger.warning(f"User {self.request.user.id} tried to delete another user's message")
            raise PermissionDenied("You cannot delete this message.")
        instance.delete()
        logger.info(f"Message deleted by user {self.request.user.id}")
    
    @action(detail=False, methods=['post'], url_path='ai-chat')
    def ai_chat(self, request):
        """
        Bridge endpoint: Accepts a user message, runs the agent, and saves both user and AI messages.
        Expects: {"conversation": <id>, "content": <user_message>}
        """
        user = request.user
        conversation_id = request.data.get("conversation")
        content = request.data.get("content", "")

        # 1. Fetch conversation and history
        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=404)

        # 2. Save user message
        user_msg = Message.objects.create(
            author="user",
            content=content,
            conversation=conversation,
            user=user
        )

        # 3. Build agent history
        history = [
            {"role": "user" if m.author == "user" else "assistant", "content": m.content}
            for m in Message.objects.filter(conversation=conversation).order_by("timestamp")
        ]

        # 4. Call the agent
        agent = ConversationalAgent()
        agent.conversation_history = history[:-1]  # All except the new user message
        result = agent.chat(content)

        # 5. Save AI response
        ai_msg = Message.objects.create(
            author="ai",
            content=result.get("response", ""),
            conversation=conversation,
            user=user,
            ai_confidence=result.get("context", {}).get("ai_confidence"),
            ai_version="gpt-4"  # Or extract from agent if available
        )

        # 6. Return both messages and suggestions
        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "ai_message": MessageSerializer(ai_msg).data,
            "suggestions": result.get("suggestions", []),
            "context": result.get("context", {})
        })

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)