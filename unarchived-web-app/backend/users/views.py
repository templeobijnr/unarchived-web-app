# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .serializers import CustomTokenObtainPairSerializer
from .models import *
from .serializers import *
import logging
from .utils import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
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
        
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Use Django's authenticate method with the found user's actual username
        # This is the most reliable way to check the password.
        auth_user = authenticate(username=user.username, password=password)

        if auth_user is not None:
            if not getattr(auth_user, 'is_verified', True):
                return Response({'error': 'Email not verified'}, status=status.HTTP_403_FORBIDDEN)

            # User authenticated and verified, generate JWT token
            refresh = RefreshToken.for_user(auth_user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': auth_user.id,
                    'username': auth_user.username,
                    'email': auth_user.email
                }
            })
        else:
            # This case handles when the user was found but the password was incorrect
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout endpoint"""
        logout(request)
        return Response({'message': 'Logout successful'})
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Get profile & preferences"""
        profile = request.user.profile
        preferences = request.user.preferences
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'profile': {
                'full_name': profile.full_name,
                'bio': profile.bio,
                'location': profile.location,
            },
            'preferences': {
                'receive_notifications': preferences.receive_notifications,
                'dark_mode': preferences.dark_mode,
                'language': preferences.language
            }
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def verify_email(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
    
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=400)
    
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        else:
            return Response({'error': 'Invalid or expired token'}, status=400)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_verification(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'message': 'Account already verified'}, status=400)

            send_verification_email(user, request)
            return Response({'message': 'Verification email resent.'})
        except User.DoesNotExist:
            return Response({'error': 'No account found with this email'}, status=404)


    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update profile & preferences"""
        profile = request.user.profile
        preferences = request.user.preferences
        profile_data = request.data.get('profile', {})
        prefs_data = request.data.get('preferences', {})

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        for attr, value in prefs_data.items():
            setattr(preferences, attr, value)

        profile.save()
        preferences.save()

        return Response({'message': 'Profile updated'})

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
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
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
                password=password,
                is_active=True  # keep user active but not verified
            )
            user.is_verified = False  # Set to False initially until email verification
            user.save()
            send_verification_email(user, request)

            return Response({
                'message': 'User created. Check your email to verify your account.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({
                'error': 'Failed to create user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view"""
    serializer_class = CustomTokenObtainPairSerializer

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Invalid activation link'}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified. You can now log in.'})
        return Response({'error': 'Activation link invalid or expired'}, status=400)

   
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
