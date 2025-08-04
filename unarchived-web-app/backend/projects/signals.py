from django.db.models.signals import post_save
from django.dispatch import receiver
from files.models import UploadedFile # 
from .analysis import trigger_ai_analysis

@receiver(post_save, sender=UploadedFile)
def project_file_post_save(sender, instance, created, **kwargs):
    """
    Trigger AI analysis when a new project file is created.
    """
    print(f"SIGNAL FIRED for file: {instance.original_filename}, Created: {created}")
    
    if created:
        trigger_ai_analysis(instance)