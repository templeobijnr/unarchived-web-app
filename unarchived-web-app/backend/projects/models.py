from django.db import models
from django.conf import settings

class ProjectStage(models.Model):
    """
    Defines the distinct stages a project can be in (e.g., Ideation, Prototyping).
    
    REASONING:
    Making this a separate model instead of a 'choices' list on the Project model is a deliberate choice.
    It allows you to add, edit, or re-order stages through the admin panel without deploying new code.
    It's far more flexible and scalable.
    """
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Defines the sequence of stages for display.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    

class Project(models.Model):

    class ProjectStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        ARCHIVED = "ARCHIVED", "Archived"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_projects')

    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    stage = models.ForeignKey(ProjectStage, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Apparel, Electronics, Home Goods")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # DATA INTEGRITY: Use PROTECT for the owner relationship.
        # REASONING: This prevents you from deleting a user who owns projects, which would otherwise
        # lead to orphaned projects or, worse, accidental data loss. The incorrect model used
        # models.CASCADE, which is dangerously destructive in this context.
        on_delete=models.PROTECT,
        # BEST PRACTICE: Use a clear related_name for reverse lookups (e.g., user.owned_projects.all()).
        related_name='owned_projects'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # BEST PRACTICE: Specify a 'through' model to add extra data (like roles) to the relationship.
        through="ProjectMember",
        related_name="projects"
    )

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    """
    This is a 'through' model. It links a User to a Project and adds extra information: their role.
    This is the foundation of our permission system.
    """
    # BEST PRACTICE: Use TextChoices for roles, for the same reasons as ProjectStatus.
    class MemberRole(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        EDITOR = 'EDITOR', 'Editor'
        VIEWER = 'VIEWER', 'Viewer'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=MemberRole.choices, default=MemberRole.VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        ordering = ['-joined_at']

    def __str__(self):
        # A more robust way to display the user's name.
        user_display = getattr(self.user, 'name', self.user.username)
        return f"{user_display} in {self.project.name} ({self.get_role_display()})"

