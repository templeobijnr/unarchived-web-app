# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

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

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)