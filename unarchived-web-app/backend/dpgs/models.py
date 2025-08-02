from django.db import models
from django.contrib.auth.models import User
from knowledge_base.models import KnowledgeChunk
class DigitalProductGenome(models.Model):
    LIFECYCLE_STAGES = [
        ('created', 'Created'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('used', 'Used in RFQ'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dpgs')
    version = models.CharField(max_length=20, default='1.0')
    summary = models.TextField(blank=True)
    data = models.JSONField(default=dict)
    stage = models.CharField(max_length=20, choices=LIFECYCLE_STAGES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    knowledge_chunks = models.ManyToManyField(KnowledgeChunk, blank=True)

    def __str__(self):
        return f"{self.title} (v{self.version})"
    
    class Meta:
        ordering = ['-created_at']

    def fetch_knowledge_for_dpg(self):
        """Fetches relevant knowledge from the knowledge base and links it to this DPG"""
        relevant_knowledge = KnowledgeChunk.objects.filter(domain="materials")  # Example domain
        self.knowledge_chunks.add(*relevant_knowledge)
        self.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from rfq.models import RFQ

@receiver(post_save, sender=DigitalProductGenome)
def auto_create_rfq(sender, instance, created, **kwargs):
    if not created and instance.stage == 'approved':
        RFQ.objects.get_or_create(
            dpg=instance,
            defaults={
                'title': f"RFQ for {instance.title}",
                'description': instance.description,
                'category': instance.data.get('category', ''),
                'status': 'draft',
                'created_by': instance.owner
            }
        )
