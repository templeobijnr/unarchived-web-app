from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Supplier, SupplierContact, SupplierVerification, RFQ, RFQDistribution, Quote, Message, KPI, CommunicationLog
from .serializers import (
    SupplierSerializer, SupplierContactSerializer, SupplierVerificationSerializer,
    RFQSerializer, RFQDistributionSerializer, QuoteSerializer, 
    MessageSerializer, KPISerializer, CommunicationLogSerializer,
    DashboardKPISerializer, RecentActivitySerializer, UpcomingDeadlineSerializer
)
from .ai_agent import sourcing_agent
from .rfq_distribution import rfq_distribution_service
from .supplier_verification import supplier_verification_service

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    """Simple authentication endpoints"""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Simple login endpoint"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout endpoint"""
        logout(request)
        return Response({'message': 'Logout successful'})
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        """Get current user info"""
        if request.user.is_authenticated:
            return Response({
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            })
        else:
            return Response(
                {'error': 'Not authenticated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )


class SupplierViewSet(viewsets.ModelViewSet):
    """Enhanced supplier management with verification"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter suppliers based on query parameters"""
        queryset = Supplier.objects.all()
        
        # Filter by verification status
        verification_status = self.request.query_params.get('verification_status')
        if verification_status:
            queryset = queryset.filter(verification_status=verification_status)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(
                Q(category=category) | Q(categories__contains=[category])
            )
        
        # Filter by region
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        
        # Filter by reliability score
        min_reliability = self.request.query_params.get('min_reliability')
        if min_reliability:
            queryset = queryset.filter(reliability__gte=int(min_reliability))
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Initiate supplier verification process"""
        try:
            supplier = self.get_object()
            verification = supplier_verification_service.initiate_verification(supplier.id)
            
            return Response({
                'message': 'Verification process initiated',
                'verification_id': verification.id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error initiating verification: {str(e)}")
            return Response({
                'error': 'Failed to initiate verification'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def submit_documents(self, request, pk=None):
        """Submit verification documents"""
        try:
            supplier = self.get_object()
            documents = request.data.get('documents', {})
            
            verification = supplier_verification_service.submit_documents(
                supplier.id, documents
            )
            
            return Response({
                'message': 'Documents submitted successfully',
                'verification_status': verification.status
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error submitting documents: {str(e)}")
            return Response({
                'error': 'Failed to submit documents'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Review and approve/reject supplier"""
        try:
            supplier = self.get_object()
            decision = request.data.get('decision')
            notes = request.data.get('notes', '')
            
            if decision not in ['approved', 'rejected']:
                return Response({
                    'error': 'Invalid decision. Must be "approved" or "rejected"'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            supplier = supplier_verification_service.review_supplier(
                supplier.id, request.user.id, decision, notes
            )
            
            return Response({
                'message': f'Supplier {decision} successfully',
                'verification_status': supplier.verification_status
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error reviewing supplier: {str(e)}")
            return Response({
                'error': 'Failed to review supplier'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        """Get supplier contacts"""
        supplier = self.get_object()
        contacts = supplier.contacts.all()
        serializer = SupplierContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def communications(self, request, pk=None):
        """Get supplier communications"""
        supplier = self.get_object()
        communications = supplier.communications.all()[:50]  # Limit to recent 50
        serializer = CommunicationLogSerializer(communications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def performance_metrics(self, request, pk=None):
        """Get supplier performance metrics"""
        supplier = self.get_object()
        
        metrics = {
            'reliability': supplier.reliability,
            'response_time_avg': supplier.response_time_avg,
            'quote_acceptance_rate': float(supplier.quote_acceptance_rate),
            'total_quotes': supplier.quotes.count(),
            'accepted_quotes': supplier.quotes.filter(status='accepted').count(),
            'total_rfqs': supplier.rfq_distributions.count(),
            'responded_rfqs': supplier.rfq_distributions.filter(status='responded').count(),
        }
        
        return Response(metrics)


class SupplierContactViewSet(viewsets.ModelViewSet):
    """Supplier contact management"""
    queryset = SupplierContact.objects.all()
    serializer_class = SupplierContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter contacts by supplier"""
        supplier_id = self.request.query_params.get('supplier_id')
        if supplier_id:
            return SupplierContact.objects.filter(supplier_id=supplier_id)
        return SupplierContact.objects.all()


class RFQViewSet(viewsets.ModelViewSet):
    """Enhanced RFQ management with distribution"""
    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter RFQs based on query parameters"""
        queryset = RFQ.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by creator
        if not self.request.user.is_staff:
            queryset = queryset.filter(created_by=self.request.user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def distribute(self, request, pk=None):
        """Distribute RFQ to suppliers"""
        try:
            rfq = self.get_object()
            distribution_method = request.data.get('distribution_method', 'auto')
            manual_supplier_ids = request.data.get('supplier_ids', [])
            
            distributions = rfq_distribution_service.distribute_rfq(
                rfq.id, distribution_method, manual_supplier_ids
            )
            
            return Response({
                'message': f'RFQ distributed to {len(distributions)} suppliers',
                'distributions': RFQDistributionSerializer(distributions, many=True).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error distributing RFQ: {str(e)}")
            return Response({
                'error': 'Failed to distribute RFQ'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def suppliers(self, request, pk=None):
        """Get suppliers for RFQ distribution"""
        rfq = self.get_object()
        
        # Get matched suppliers
        matched_suppliers = rfq_distribution_service.auto_match_suppliers(rfq)
        
        # Get already distributed suppliers
        distributed_suppliers = rfq.distributions.values_list('supplier_id', flat=True)
        
        # Filter out already distributed suppliers
        available_suppliers = [
            supplier for supplier in matched_suppliers 
            if supplier.id not in distributed_suppliers
        ]
        
        serializer = SupplierSerializer(available_suppliers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def responses(self, request, pk=None):
        """Get RFQ responses and quotes"""
        rfq = self.get_object()
        quotes = rfq.quotes.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def distribution_stats(self, request, pk=None):
        """Get RFQ distribution statistics"""
        rfq = self.get_object()
        stats = rfq_distribution_service.get_distribution_stats(rfq.id)
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        """Track RFQ view by supplier"""
        try:
            rfq = self.get_object()
            supplier_id = request.data.get('supplier_id')
            
            if not supplier_id:
                return Response({
                    'error': 'supplier_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            rfq_distribution_service.track_rfq_view(rfq.id, supplier_id)
            
            return Response({
                'message': 'View tracked successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error tracking RFQ view: {str(e)}")
            return Response({
                'error': 'Failed to track view'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuoteViewSet(viewsets.ModelViewSet):
    """Quote management"""
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Create quote and track response"""
        try:
            response = super().create(request, *args, **kwargs)
            
            # Track RFQ response
            quote = Quote.objects.get(id=response.data['id'])
            rfq_distribution_service.track_rfq_response(
                quote.rfq.id, quote.supplier.id
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating quote: {str(e)}")
            return Response({
                'error': 'Failed to create quote'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a quote"""
        try:
            quote = self.get_object()
            quote.status = 'accepted'
            quote.save()
            
            # Update supplier metrics
            supplier = quote.supplier
            total_quotes = supplier.quotes.count()
            accepted_quotes = supplier.quotes.filter(status='accepted').count()
            supplier.quote_acceptance_rate = (accepted_quotes / total_quotes * 100) if total_quotes > 0 else 0
            supplier.save()
            
            return Response({
                'message': 'Quote accepted successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error accepting quote: {str(e)}")
            return Response({
                'error': 'Failed to accept quote'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a quote"""
        try:
            quote = self.get_object()
            quote.status = 'rejected'
            quote.save()
            
            return Response({
                'message': 'Quote rejected successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error rejecting quote: {str(e)}")
            return Response({
                'error': 'Failed to reject quote'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageViewSet(viewsets.ModelViewSet):
    """Chat message management"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter messages by user"""
        return Message.objects.filter(user=self.request.user)


class KPIViewSet(viewsets.ModelViewSet):
    """KPI management"""
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter KPIs by user"""
        return KPI.objects.filter(user=self.request.user)


class CommunicationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Communication log management (read-only)"""
    queryset = CommunicationLog.objects.all()
    serializer_class = CommunicationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter communications by user's suppliers"""
        user = self.request.user
        
        # Get suppliers associated with user's RFQs
        user_supplier_ids = RFQDistribution.objects.filter(
            rfq__created_by=user
        ).values_list('supplier_id', flat=True).distinct()
        
        return CommunicationLog.objects.filter(supplier_id__in=user_supplier_ids)


# Authentication views
# JWT imports already added at the top of the file

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer with additional user data"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_staff'] = self.user.is_staff
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view"""
    serializer_class = CustomTokenObtainPairSerializer


# User registration view
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not all([username, email, password]):
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'message': 'User created successfully',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return Response({
            'error': 'Failed to create user'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
