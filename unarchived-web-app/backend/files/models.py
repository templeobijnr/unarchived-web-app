from django.db import models
from django.conf import settings
from projects.models import Project

class UploadedFile(models.Model):
    """Represents any single file uploaded by a user to the system."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_files"
    )

    file = models.FileField(upload_to='project_files/')

    original_filename = models.CharField(
        max_length=255,
        blank=True,
        help_text="The name of the file as it was on the user's computer."
    )
    file_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="The MIME type of the file, e.g., 'application/pdf', 'image/jpeg'."
    )
    size = models.PositiveIntegerField(
        help_text="File size in bytes."
    )

    # --- Status for AI Processing ---
    class ProcessingStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Upload'
        UPLOADED = 'UPLOADED', 'Uploaded'
        PROCESSING = 'PROCESSING', 'AI Processing'
        COMPLETED = 'COMPLETED', 'Processing Complete'
        FAILED = 'FAILED', 'Processing Failed'

    status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.UPLOADED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename
