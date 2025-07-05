# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from ..models import *
from ..serializers import *
from ..rfq_distribution import rfq_distribution_service
from ..supplier_verification import supplier_verification_service
import logging

logger = logging.getLogger(__name__)

class MessageViewSet(viewsets.ModelViewSet):
    """Chat message management"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter messages by user"""
        return Message.objects.filter(user=self.request.user)