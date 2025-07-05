from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
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
    
    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.author}: {self.content[:50]}..."