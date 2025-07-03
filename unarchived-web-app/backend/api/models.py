from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone









class KPI(models.Model):
    """Key Performance Indicators model"""
    id = models.AutoField(primary_key=True)
    saved_cost = models.DecimalField(max_digits=12, decimal_places=2)
    quotes_in_flight = models.IntegerField()
    on_time_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage")
    total_orders = models.IntegerField()
    active_suppliers = models.IntegerField()
    avg_lead_time = models.IntegerField(help_text="Average lead time in days")
    
    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpis')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"KPI for {self.user.username} - {self.created_at.date()}"
