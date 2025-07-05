from django.db import models
from suppliers.models import Supplier
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class RFQ(models.Model):
    """Enhanced RFQ with distribution capabilities"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('distributed', 'Distributed to Suppliers'),
        ('quotes_received', 'Quotes Received'),
        ('evaluating', 'Evaluating Quotes'),
        ('awarded', 'Awarded'),
        ('closed', 'Closed'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    
    # Quantities & Pricing
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    budget_range = models.CharField(max_length=100, blank=True)  # "$10,000 - $15,000"
    
    # Timeline
    deadline = models.DateTimeField()
    quote_deadline = models.DateTimeField(null=True, blank=True)
    delivery_deadline = models.DateTimeField(null=True, blank=True)
    
    # Distribution Settings
    distribution_method = models.CharField(
        max_length=20,
        choices=[
            ('auto', 'Automatic - AI Matched'),
            ('manual', 'Manual Selection'),
            ('hybrid', 'Hybrid - AI + Manual')
        ],
        default='auto'
    )
    target_supplier_count = models.IntegerField(default=10)
    regions_preferred = models.JSONField(default=list)
    supplier_criteria = models.JSONField(default=dict)
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    responses = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    # Foreign keys
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rfqs')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['deadline']),
            models.Index(fields=['distribution_method']),
        ]
    
    def __str__(self):
        return self.title


class RFQDistribution(models.Model):
    """Track RFQ distribution to suppliers"""
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('viewed', 'Viewed'),
        ('responded', 'Responded'),
        ('failed', 'Failed'),
    ]
    
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='distributions')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='rfq_distributions')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Communication tracking
    email_sent = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['rfq', 'supplier']
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.rfq.title} -> {self.supplier.name} ({self.status})"
