from rest_framework import serializers
from ..models import *

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