# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from .models import *
from .serializers import *
from .permissions import IsProjectMember, IsProjectOwner
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rfq.models import RFQ
from quotes.models import Quote
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

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

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(collaborators=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(user=self.request.user, project=project, role='owner')
    
    @action(detail=True, methods=['get'], permission_classes=[IsProjectOwner])
    def members(self, request, pk=None):
        """List project members"""
        project = self.get_object()
        members = ProjectMember.objects.filter(project=project)
        serializer = ProjectMemberSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsProjectOwner, permissions.IsAuthenticated])
    def add_member(self, request, pk=None):
        """Add a new member"""
        project = self.get_object()
        serializer = ProjectMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsProjectOwner])
    def update_member(self, request, pk=None):
        """Update member role"""
        project = self.get_object()
        user_id = request.data.get('user')
        try:
            member = ProjectMember.objects.get(project=project, user_id=user_id)
            member.role = request.data.get('role', member.role)
            member.save()
            return Response(ProjectMemberSerializer(member).data)
        except ProjectMember.DoesNotExist:
            return Response({'error': 'Member not found'}, status=404)

    @action(detail=True, methods=['delete'], permission_classes=[IsProjectOwner])
    def remove_member(self, request, pk=None):
        """Remove a project member"""
        project = self.get_object()
        user_id = request.data.get('user')
        if not user_id:
            return Response({'error': 'user field is required'}, status=400)
        deleted, _ = ProjectMember.objects.filter(project=project, user_id=user_id).delete()
        if deleted:
            return Response({'message': 'Member removed'})
        return Response({'error': 'Member not found'}, status=404)
    
    def get_object(self):
        # This allows detail routes to fetch any project (then check permissions)
        return get_object_or_404(Project, pk=self.kwargs["pk"])

