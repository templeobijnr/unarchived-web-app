# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from ..models import *
from ..serializers import *
from ..rfq_distribution import rfq_distribution_service
from ..supplier_verification import supplier_verification_service
import logging

logger = logging.getLogger(__name__)

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