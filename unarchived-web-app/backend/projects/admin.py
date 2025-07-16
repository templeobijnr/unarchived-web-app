from django.contrib import admin
from .models import (
     Project,
     ProjectMember,
     ProjectStage,
)

# Custom Admin Views for better usability


# Register other models directly for simplicity

admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectStage)