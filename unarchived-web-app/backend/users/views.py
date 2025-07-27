# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *
from rfq.rfq_distribution import rfq_distribution_service
from suppliers.supplier_verification import supplier_verification_service
import logging

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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Allow login with email
        email = attrs.get("username")  # still comes as 'username' from the request
        try:
            user = User.objects.get(email=email)
            attrs["username"] = user.username  # override with actual username
        except User.DoesNotExist:
            pass  # Let JWT handle the error normally

        return super().validate(attrs)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view"""
    serializer_class = CustomTokenObtainPairSerializer

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
        
        
def login_test_ui(request):
    return render(request, 'login_test.html')


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt  
def register_user_ui(request):
    """Handles registration from a browser form"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([username, email, password]):
            return render(request, 'register.html', {'error': 'All fields are required'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        return render(request, 'register.html', {'message': 'Registration successful!'})

    return render(request, 'register.html')
