# Auto-split from original views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .serializers import *
from .permissions import IsProjectMember, IsProjectOwner
from django.db.models import Q
from rest_framework.generics import get_object_or_404
import logging
from .analysis import trigger_ai_analysis

logger = logging.getLogger(__name__)
User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct().order_by('-created_at')

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(user=self.request.user, project=project, role=ProjectMember.MemberRole.OWNER)
    
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

    @action(detail=True, methods=["get"])
    def context(self, request, pk=None):
        project = self.get_object()
        context = ProjectContextEngine.objects.filter(project=project).first()
        uploads = ProjectUpload.objects.filter(project=project)

        return Response({
            "context_summary": ProjectContextEngineSerializer(context).data if context else {},
            "uploads": ProjectUploadSerializer(uploads, many=True).data
        })

    @action(detail=True, methods=["post"])
    def ignite(self, request, pk=None):
        # Re-analyze all uploaded files
        project = self.get_object()
        files = project.projectfile_set.all()

        for file in files:
            trigger_ai_analysis(file)

        return Response({"message": "AI analysis triggered for all files."})

class ProjectStageViewSet(viewsets.ModelViewSet):
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer
    permission_classes = [permissions.IsAdminUser]

