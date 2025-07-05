from rest_framework import serializers
from .models import (
    Supplier, SupplierContact, SupplierVerification, RFQ, RFQDistribution,
    Quote, Message, KPI, CommunicationLog
)
from django.contrib.auth.models import User





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