from django.contrib import admin
from .models import User, UserProfile, UserPreferences

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified', 'is_active', 'is_staff')
    list_filter = ('is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')
    search_fields = ('user__username', 'full_name', 'location')
    ordering = ('user__username',)
    raw_id_fields = ('user',)

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_notifications', 'dark_mode', 'language')
    search_fields = ('user__username',)
    ordering = ('user__username',)
    raw_id_fields = ('user',)