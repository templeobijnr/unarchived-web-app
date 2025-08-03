from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, UserPreferences
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'bio', 'avatar', 'location')

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ('receive_notifications', 'dark_mode', 'language')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email_or_username = attrs.get("username")  # DRF sends this key by default
        password = attrs.get("password")

        # Try to resolve email to username
        try:
            user = User.objects.get(email=email_or_username)
            attrs["username"] = user.username
            logger.info(f"User found: {user.username}")
        except User.DoesNotExist:
            logger.warning(f"User with email {email_or_username} not found!")
            # Fall back to using username directly
            pass

        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError("Email is not verified")

        return data

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    preferences = UserPreferencesSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile', 'preferences']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
        }
