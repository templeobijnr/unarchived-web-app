from rest_framework import serializers
from .models import *

class RecentActivitySerializer(serializers.Serializer):
    """Recent activity serializer"""
    type = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
    status = serializers.CharField()

class UpcomingDeadlineSerializer(serializers.Serializer):
    """Upcoming deadline serializer"""
    rfq_id = serializers.IntegerField()
    title = serializers.CharField()
    deadline = serializers.DateTimeField()
    days_remaining = serializers.IntegerField()
    status = serializers.CharField() 

class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = ['id', 'name', 'order']

class ProjectSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    stage = serializers.SlugRelatedField(slug_field='name', queryset=ProjectStage.objects.all(), required=False, allow_null=True)
    dpg_count = serializers.IntegerField(read_only=True, default=0)
    file_count = serializers.IntegerField(read_only=True, default=0)
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'stage', 'category',
            'owner', 'parent', 'created_at', 'updated_at', 'role',
            'dpg_count', 'file_count'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_role(self, obj):
        user = self.context['request'].user
        try:
            return obj.memberships.get(user=user).role
        except ProjectMember.DoesNotExist:
            return None

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    role = serializers.ChoiceField(choices=ProjectMember.MemberRole.choices)
    
    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'user_username', 'user_email', 'role', 'joined_at']
        read_only_fields = ['project', 'joined_at', 'user_username', 'user_email']
        
class ProjectUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUpload
        fields = "__all__"


class ProjectContextEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContextEngine
        fields = "__all__"
