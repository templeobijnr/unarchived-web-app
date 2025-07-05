from django.db import models
from suppliers.models import Supplier
from rfq.models import RFQ
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.


class Quote(models.Model):
    """Quote model for supplier responses to RFQs"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    id = models.AutoField(primary_key=True)
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='quotes')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='quotes')
    product = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    lead_time = models.IntegerField(help_text="Lead time in days")
    moq = models.IntegerField(help_text="Minimum order quantity")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    specs = models.JSONField(default=dict, help_text="Product specifications")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['rfq', 'supplier']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.product}"
