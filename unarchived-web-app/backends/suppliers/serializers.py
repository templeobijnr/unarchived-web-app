
from rest_framework import serializers
from .models import (
    Supplier, SupplierContact, SupplierVerification,
     CommunicationLog
)
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
