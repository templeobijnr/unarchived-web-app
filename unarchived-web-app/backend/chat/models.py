from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    """Chat message model for AI assistant conversations"""
    AUTHOR_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=10, choices=AUTHOR_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    typing = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    ai_confidence = models.FloatField(null=True, blank=True)
    ai_version = models.CharField(max_length=32, null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.author}: {self.content[:50]}..."