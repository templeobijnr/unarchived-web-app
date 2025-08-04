from rest_framework import permissions
from .models import ProjectMember, Project

class IsProjectMember(permissions.BasePermission):
    """
    Custom permission that handles all project-related access.
    - Authenticated users can create projects.
    - Authenticated users can list projects (the view should filter this list).
    - Only project members can view/edit a specific project based on their role.
    """

    def has_permission(self, request, view):
        # Allow list and create actions for any authenticated user.
        # The view's get_queryset will be responsible for filtering the list.
        if view.action in ['list', 'create']:
            return request.user and request.user.is_authenticated

        # For all other actions (retrieve, update, etc.), they are on a specific
        # project, so we require the user to be a project member.
        project_pk = view.kwargs.get('pk') or view.kwargs.get('project_pk')
        if not project_pk:
            return False

        return ProjectMember.objects.filter(user=request.user, project_id=project_pk).exists()

    def has_object_permission(self, request, view, obj):
        # This method is called for detail views after has_permission passes.
        # 'obj' here is the Project instance.
        try:
            member = ProjectMember.objects.get(user=request.user, project=obj)

            # SAFE_METHODS are GET, HEAD, OPTIONS. All members can view.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Allow owners and editors to make changes.
            return member.role in [ProjectMember.MemberRole.OWNER, ProjectMember.MemberRole.EDITOR]

        except ProjectMember.DoesNotExist:
            return False


class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow project owners to perform an action.
    This is useful for sensitive actions like adding/removing members.
    """
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('pk') or view.kwargs.get('project_pk')
        if not project_pk:
            return False

        try:
            project = Project.objects.get(pk=project_pk)
            return ProjectMember.objects.filter(
                user=request.user,
                project=project,
                role=ProjectMember.MemberRole.OWNER
            ).exists()
        except Project.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # 'obj' here is the Project instance.
        return ProjectMember.objects.filter(
            project=obj, user=request.user, role=ProjectMember.MemberRole.OWNER
        ).exists()