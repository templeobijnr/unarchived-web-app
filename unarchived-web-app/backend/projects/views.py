# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from .models import *
from .serializers import *

import logging

logger = logging.getLogger(__name__)

class KPIViewSet(viewsets.ModelViewSet):
    """KPI management"""
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter KPIs by user"""
        return KPI.objects.filter(user=self.request.user)

class DashboardViewSet(viewsets.ViewSet):
    """API endpoint for dashboard data"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def kpis(self, request):
        """Get dashboard KPIs"""
        user = request.user
        
        # Calculate KPIs from actual data
        quotes_in_flight = Quote.objects.filter(
            rfq__created_by=user,
            status='pending'
        ).count()
        
        # Get the latest KPI record or create default values
        try:
            latest_kpi = KPI.objects.filter(user=user).latest('created_at')
            kpi_data = {
                'saved_cost': float(latest_kpi.saved_cost),
                'quotes_in_flight': quotes_in_flight,
                'on_time_rate': float(latest_kpi.on_time_rate),
                'avg_lead_time': latest_kpi.avg_lead_time
            }
        except KPI.DoesNotExist:
            # Default values if no KPI data exists
            kpi_data = {
                'saved_cost': 285000.00,
                'quotes_in_flight': quotes_in_flight,
                'on_time_rate': 94.2,
                'avg_lead_time': 18
            }
        
        serializer = DashboardKPISerializer(kpi_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_activity(self, request):
        """Get recent activity for dashboard"""
        user = request.user
        
        # Mock recent activity data (in a real app, this would come from actual events)
        recent_activity = [
            {
                'id': 1,
                'type': 'quote_received',
                'title': 'New quote received',
                'description': 'Shenzhen Tech Cases submitted quote for phone cases',
                'time': '2 minutes ago',
                'icon': 'Quote',
                'color': 'text-blue-400'
            },
            {
                'id': 2,
                'type': 'rfq_created',
                'title': 'RFQ published',
                'description': 'Bluetooth headphones RFQ sent to 8 suppliers',
                'time': '1 hour ago',
                'icon': 'Package',
                'color': 'text-green-400'
            },
            {
                'id': 3,
                'type': 'supplier_verified',
                'title': 'Supplier verified',
                'description': 'Premium Cases Co completed verification process',
                'time': '3 hours ago',
                'icon': 'Users',
                'color': 'text-purple-400'
            },
            {
                'id': 4,
                'type': 'shipment_update',
                'title': 'Shipment departed',
                'description': 'Order #1847 left Shenzhen Port',
                'time': '5 hours ago',
                'icon': 'MapPin',
                'color': 'text-yellow-400'
            }
        ]
        
        serializer = RecentActivitySerializer(recent_activity, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming_deadlines(self, request):
        """Get upcoming RFQ deadlines"""
        user = request.user
        
        # Get RFQs with upcoming deadlines
        upcoming_rfqs = RFQ.objects.filter(
            created_by=user,
            status='published',
            deadline__gte=datetime.now()
        ).order_by('deadline')[:5]
        
        deadlines = []
        for rfq in upcoming_rfqs:
            responses = Quote.objects.filter(rfq=rfq).count()
            status = 'urgent' if rfq.deadline <= datetime.now() + timedelta(days=3) else 'normal'
            
            deadlines.append({
                'id': rfq.id,
                'title': rfq.title,
                'deadline': rfq.deadline.date(),
                'status': status,
                'responses': responses
            })
        
        serializer = UpcomingDeadlineSerializer(deadlines, many=True)
        return Response(serializer.data)