from rest_framework import serializers
from .models import (
   RFQ, RFQDistribution,
    
)


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

