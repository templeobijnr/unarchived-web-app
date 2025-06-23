from rest_framework import serializers
from .models import (
    Supplier, SupplierContact, SupplierVerification, RFQ, RFQDistribution,
    Quote, Message, KPI, CommunicationLog
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SupplierSerializer(serializers.ModelSerializer):
    """Enhanced supplier serializer with verification status"""
    
    verification_status_display = serializers.CharField(
        source='get_verification_status_display', 
        read_only=True
    )
    contacts_count = serializers.SerializerMethodField()
    recent_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'legal_name', 'logo', 'verification_status', 
            'verification_status_display', 'verification_date', 'verified_by',
            'business_type', 'year_established', 'employee_count', 'annual_revenue',
            'certifications', 'quality_standards', 'audit_reports',
            'contact_email', 'contact_phone', 'contact_address', 'website',
            'region', 'country', 'shipping_regions', 'lead_time_range',
            'reliability', 'response_time_avg', 'quote_acceptance_rate',
            'category', 'categories', 'capabilities', 'product_catalog',
            'payment_terms', 'minimum_order_value', 'credit_rating',
            'created_at', 'updated_at', 'last_activity',
            'contacts_count', 'recent_activity'
        ]
        read_only_fields = [
            'verification_date', 'verified_by', 'created_at', 'updated_at', 
            'last_activity', 'contacts_count', 'recent_activity'
        ]
    
    def get_contacts_count(self, obj):
        return obj.contacts.count()
    
    def get_recent_activity(self, obj):
        # Get recent communications
        recent_communications = obj.communications.all()[:5]
        return [
            {
                'type': comm.communication_type,
                'subject': comm.subject,
                'date': comm.created_at.isoformat()
            }
            for comm in recent_communications
        ]


class SupplierContactSerializer(serializers.ModelSerializer):
    """Supplier contact serializer"""
    
    contact_type_display = serializers.CharField(
        source='get_contact_type_display', 
        read_only=True
    )
    preferred_contact_method_display = serializers.CharField(
        source='get_preferred_contact_method_display', 
        read_only=True
    )
    
    class Meta:
        model = SupplierContact
        fields = [
            'id', 'supplier', 'contact_type', 'contact_type_display',
            'name', 'title', 'email', 'phone', 'mobile', 'wechat', 'whatsapp',
            'preferred_contact_method', 'preferred_contact_method_display',
            'timezone', 'working_hours', 'is_active', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SupplierVerificationSerializer(serializers.ModelSerializer):
    """Supplier verification serializer"""
    
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = SupplierVerification
        fields = [
            'id', 'supplier', 'supplier_name', 'status', 'status_display',
            'documents_required', 'documents_submitted',
            'reviewer', 'reviewer_name', 'review_notes', 'review_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'supplier_name', 'reviewer_name'
        ]


class RFQSerializer(serializers.ModelSerializer):
    """Enhanced RFQ serializer with distribution capabilities"""
    
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    distribution_method_display = serializers.CharField(
        source='get_distribution_method_display', 
        read_only=True
    )
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    quotes_count = serializers.SerializerMethodField()
    distribution_stats = serializers.SerializerMethodField()
    
    class Meta:
        model = RFQ
        fields = [
            'id', 'title', 'description', 'category', 'subcategory',
            'quantity', 'target_price', 'currency', 'budget_range',
            'deadline', 'quote_deadline', 'delivery_deadline',
            'distribution_method', 'distribution_method_display',
            'target_supplier_count', 'regions_preferred', 'supplier_criteria',
            'status', 'status_display', 'responses', 'views',
            'created_by', 'created_by_name', 'created_at', 'updated_at', 'published_at',
            'quotes_count', 'distribution_stats'
        ]
        read_only_fields = [
            'created_by', 'created_by_name', 'created_at', 'updated_at', 
            'published_at', 'quotes_count', 'distribution_stats'
        ]
    
    def get_quotes_count(self, obj):
        return obj.quotes.count()
    
    def get_distribution_stats(self, obj):
        distributions = obj.distributions.all()
        total = distributions.count()
        if total == 0:
            return {
                'total_sent': 0,
                'delivered': 0,
                'viewed': 0,
                'responded': 0,
                'delivery_rate': 0,
                'response_rate': 0
            }
        
        delivered = distributions.filter(status='delivered').count()
        viewed = distributions.filter(status='viewed').count()
        responded = distributions.filter(status='responded').count()
        
        return {
            'total_sent': total,
            'delivered': delivered,
            'viewed': viewed,
            'responded': responded,
            'delivery_rate': (delivered / total * 100) if total > 0 else 0,
            'response_rate': (responded / total * 100) if total > 0 else 0
        }


class RFQDistributionSerializer(serializers.ModelSerializer):
    """RFQ distribution serializer"""
    
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    rfq_title = serializers.CharField(source='rfq.title', read_only=True)
    
    class Meta:
        model = RFQDistribution
        fields = [
            'id', 'rfq', 'rfq_title', 'supplier', 'supplier_name',
            'status', 'status_display', 'sent_at', 'delivered_at', 
            'viewed_at', 'responded_at', 'email_sent', 'notification_sent'
        ]
        read_only_fields = [
            'sent_at', 'delivered_at', 'viewed_at', 'responded_at',
            'email_sent', 'notification_sent', 'supplier_name', 'rfq_title'
        ]


class QuoteSerializer(serializers.ModelSerializer):
    """Enhanced quote serializer"""
    
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    rfq_title = serializers.CharField(source='rfq.title', read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            'id', 'rfq', 'rfq_title', 'supplier', 'supplier_name',
            'product', 'price', 'currency', 'lead_time', 'moq', 'status',
            'status_display', 'specs', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'supplier_name', 'rfq_title'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Chat message serializer"""
    
    author_display = serializers.CharField(
        source='get_author_display', 
        read_only=True
    )
    
    class Meta:
        model = Message
        fields = [
            'id', 'author', 'author_display', 'content', 'timestamp', 'typing'
        ]
        read_only_fields = ['timestamp']


class KPISerializer(serializers.ModelSerializer):
    """KPI serializer"""
    
    class Meta:
        model = KPI
        fields = [
            'id', 'saved_cost', 'quotes_in_flight', 'on_time_rate',
            'total_orders', 'active_suppliers', 'avg_lead_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CommunicationLogSerializer(serializers.ModelSerializer):
    """Communication log serializer"""
    
    communication_type_display = serializers.CharField(
        source='get_communication_type_display', 
        read_only=True
    )
    direction_display = serializers.CharField(
        source='get_direction_display', 
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    initiated_by_name = serializers.CharField(source='initiated_by.username', read_only=True)
    
    class Meta:
        model = CommunicationLog
        fields = [
            'id', 'supplier', 'supplier_name', 'contact', 'contact_name',
            'communication_type', 'communication_type_display',
            'subject', 'content', 'direction', 'direction_display',
            'initiated_by', 'initiated_by_name', 'related_rfq', 'related_quote',
            'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'supplier_name', 'contact_name', 
            'initiated_by_name'
        ]


# Dashboard serializers
class DashboardKPISerializer(serializers.Serializer):
    """Dashboard KPI summary serializer"""
    total_suppliers = serializers.IntegerField()
    verified_suppliers = serializers.IntegerField()
    pending_verifications = serializers.IntegerField()
    active_rfqs = serializers.IntegerField()
    total_quotes = serializers.IntegerField()
    avg_response_time = serializers.FloatField()
    total_savings = serializers.DecimalField(max_digits=12, decimal_places=2)


class RecentActivitySerializer(serializers.Serializer):
    """Recent activity serializer"""
    type = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
    status = serializers.CharField()


class UpcomingDeadlineSerializer(serializers.Serializer):
    """Upcoming deadline serializer"""
    rfq_id = serializers.IntegerField()
    title = serializers.CharField()
    deadline = serializers.DateTimeField()
    days_remaining = serializers.IntegerField()
    status = serializers.CharField() 