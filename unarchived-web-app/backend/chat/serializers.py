from rest_framework import serializers
from .models import Message, Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Chat message serializer"""
    
    author_display = serializers.CharField(
        source='get_author_display', 
        read_only=True
    )
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )
    
    class Meta:
        model = Message
        fields = [
            'id', 'author', 'author_display', 'content', 'timestamp', 'typing',
            'is_read', 'ai_confidence', 'ai_version', 'conversation', 'user'
        ]
        read_only_fields = ['timestamp']