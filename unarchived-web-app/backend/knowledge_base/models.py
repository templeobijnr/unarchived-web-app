from django.db import models

import uuid
from django.db import models
from pgvector.django import VectorField

class KnowledgeChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    embedding = VectorField(dimensions=1536)
    domain = models.CharField(max_length=50, db_index=True)
    subdomain = models.CharField(max_length=100, db_index=True, blank=True)
    entity_name = models.CharField(max_length=100, db_index=True, blank=True)
    source_document = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, default='internal_manual')
    confidence_score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"[{self.domain.upper()}] {self.entity_name or 'Chunk'} from {self.source_document}"
