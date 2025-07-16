from rest_framework import permissions
from .models import ProjectMember, Project

class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow project members to view or edit.
    Role-based access:
        - viewer: read-only
        - editor: read/write
        - owner: full access
    """

    def has_object_permission(self, request, view, obj):
        try:
            member = ProjectMember.objects.get(user=request.user, project=obj)
            if request.method in permissions.SAFE_METHODS:
                return True  # All roles can read
            elif member.role == 'owner':
                return True  # Owner has full access
            elif member.role == 'editor':
                return request.method in ['PUT', 'PATCH']
            else:  # viewer
                return False
        except ProjectMember.DoesNotExist:
            return False

class IsProjectOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        # For detail routes like /projects/<id>/add_member/
        if view.kwargs.get('pk'):
            try:
                project = Project.objects.get(pk=view.kwargs['pk'])
                return ProjectMember.objects.filter(user=request.user, project=project, role='owner').exists()
            except Project.DoesNotExist:
                return False
        return False
    
    def has_object_permission(self, request, view, obj):
        return ProjectMember.objects.filter(user=request.user, project=obj, role='owner').exists()