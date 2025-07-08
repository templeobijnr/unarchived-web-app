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
from rfq.rfq_distribution import rfq_distribution_service
from suppliers.supplier_verification import supplier_verification_service
import logging

logger = logging.getLogger(__name__)

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