from django.contrib import admin
from .models import (
     KPI, 
     Project,
     ProjectMember,
)

# Custom Admin Views for better usability


# Register other models directly for simplicity


admin.site.register(KPI)
admin.site.register(Project)
admin.site.register(ProjectMember)