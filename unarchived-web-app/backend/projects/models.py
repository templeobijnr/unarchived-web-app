from django.db import models
from django.contrib.auth.models import User
class KPI(models.Model):
    """Key Performance Indicators model"""
    id = models.AutoField(primary_key=True)
    saved_cost = models.DecimalField(max_digits=12, decimal_places=2)
    quotes_in_flight = models.IntegerField()
    on_time_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage")
    total_orders = models.IntegerField()
    active_suppliers = models.IntegerField()
    avg_lead_time = models.IntegerField(help_text="Average lead time in days")
    
    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpis')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"KPI for {self.user.username} - {self.created_at.date()}"
    
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, through='ProjectMember')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"

