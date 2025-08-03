from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Supplier(models.Model):
    """Enhanced supplier model with verification system"""
    
    # Basic Information
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    logo = models.URLField(max_length=500, blank=True)
    
    # Verification Status
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_suppliers'
    )
    
    # Business Information
    business_type = models.CharField(max_length=100, blank=True)  # Manufacturer, Trading Company, etc.
    year_established = models.IntegerField(null=True, blank=True)
    employee_count = models.CharField(max_length=50, blank=True)
    annual_revenue = models.CharField(max_length=100, blank=True)
    
    # Certifications & Quality
    certifications = models.JSONField(default=list)
    quality_standards = models.JSONField(default=list)  # ISO, CE, RoHS, etc.
    audit_reports = models.JSONField(default=list)
    
    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50)
    contact_address = models.TextField()
    website = models.URLField(blank=True)
    
    # Location & Shipping
    region = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True)
    shipping_regions = models.JSONField(default=list)
    lead_time_range = models.CharField(max_length=100, blank=True)  # "7-14 days"
    
    # Performance Metrics
    reliability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Reliability score from 0-100",
        default=50
    )
    response_time_avg = models.IntegerField(
        help_text="Average response time in hours",
        default=48
    )
    quote_acceptance_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Percentage of accepted quotes",
        default=0.0
    )
    
    # Categories & Capabilities
    category = models.CharField(max_length=100)  # Keep for backward compatibility
    categories = models.JSONField(default=list)
    capabilities = models.JSONField(default=list)
    product_catalog = models.JSONField(default=list)
    
    # Financial & Payment
    payment_terms = models.CharField(max_length=100, blank=True)
    minimum_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    credit_rating = models.CharField(max_length=10, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reliability', '-verification_status', 'name']
        indexes = [
            models.Index(fields=['verification_status']),
            models.Index(fields=['categories']),
            models.Index(fields=['region']),
            models.Index(fields=['reliability']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.verification_status})"

class SupplierContact(models.Model):
    """Supplier contact management"""
    
    CONTACT_TYPE_CHOICES = [
        ('primary', 'Primary Contact'),
        ('sales', 'Sales Contact'),
        ('technical', 'Technical Contact'),
        ('quality', 'Quality Contact'),
        ('logistics', 'Logistics Contact'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    
    # Contact Information
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    wechat = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=100, blank=True)
    
    # Communication Preferences
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('wechat', 'WeChat'),
            ('whatsapp', 'WhatsApp'),
        ],
        default='email'
    )
    timezone = models.CharField(max_length=50, blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['supplier', 'contact_type']
        ordering = ['supplier', 'contact_type']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.get_contact_type_display()}: {self.name}"

class SupplierVerification(models.Model):
    """Supplier verification process tracking"""
    
    STATUS_CHOICES = [
        ('initiated', 'Verification Initiated'),
        ('documents_requested', 'Documents Requested'),
        ('documents_received', 'Documents Received'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    supplier = models.OneToOneField(Supplier, on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    
    # Documents
    documents_required = models.JSONField(default=list)
    documents_submitted = models.JSONField(default=dict)
    
    # Review
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    review_notes = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Verification for {self.supplier.name} - {self.status}"

class CommunicationLog(models.Model):
    """Track all communications with suppliers"""
    
    COMMUNICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('chat', 'Chat'),
        ('rfq', 'RFQ'),
        ('quote', 'Quote'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='communications')
    contact = models.ForeignKey(SupplierContact, on_delete=models.SET_NULL, null=True, blank=True)
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE_CHOICES)
    
    # Communication Details
    subject = models.CharField(max_length=255)
    content = models.TextField()
    direction = models.CharField(max_length=10, choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')])
    
    # Metadata
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    related_rfq = models.ForeignKey("rfq.RFQ", on_delete=models.SET_NULL, null=True, blank=True)
    related_quote = models.ForeignKey('quotes.Quote', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('replied', 'Replied'),
            ('failed', 'Failed'),
        ],
        default='sent'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['supplier', 'communication_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.supplier.name} - {self.communication_type}: {self.subject}"