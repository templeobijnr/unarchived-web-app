from django.db import models
from django.conf import settings
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dpgs')
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

class DPGComponent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    dpg = models.ForeignKey(DigitalProductGenome, related_name='components', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Order in which the component is placed in the spec sheet")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Component: {self.name} for {self.dpg.title}"

class ComponentSpecification(models.Model):
    component = models.ForeignKey(DPGComponent, related_name='specifications', on_delete=models.CASCADE)
    material = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Specification for {self.component.name} - Material: {self.material}"


class ApparelDPGExtension(models.Model):
    dpg = models.OneToOneField(DigitalProductGenome, related_name='apparel_extension', on_delete=models.CASCADE)
    fabric_composition = models.TextField(blank=True)
    sizing_chart = models.JSONField(default=dict)
    fit_information = models.TextField(blank=True)
    construction_details = models.TextField(blank=True)
    hardware_components = models.JSONField(default=dict)
    colorways = models.JSONField(default=dict)
    cost_breakdown = models.JSONField(default=dict)
    manufacturing_data = models.JSONField(default=dict)

    def __str__(self):
        return f"Apparel Specifics for {self.dpg.title}"

class GeneratedAsset(models.Model):
    dpg = models.ForeignKey(DigitalProductGenome, related_name='assets', on_delete=models.CASCADE)
    file = models.FileField(upload_to='assets/', null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asset for {self.dpg.title} ({self.file.name})"

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
