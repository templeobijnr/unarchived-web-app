from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('docx', 'DOCX'),
        ('xlsx', 'XLSX'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    parsed_output = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='uploaded')  # uploaded, processing, done, failed

    def __str__(self):
        return f"{self.file.name} - {self.file_type}"