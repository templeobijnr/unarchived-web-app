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
        from suppliers.serializers import SupplierSerializer
        serializer = SupplierSerializer(available_suppliers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def responses(self, request, pk=None):
        """Get RFQ responses and quotes"""
        rfq = self.get_object()
        quotes = rfq.quotes.all()
        from quotes.serializers import QuoteSerializer
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