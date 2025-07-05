
from rest_framework import viewsets, permissions, filters
from .models import DigitalProductGenome
from .serializers import DigitalProductGenomeSerializer

class DigitalProductGenomeViewSet(viewsets.ModelViewSet):
    serializer_class = DigitalProductGenomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'version']
    ordering_fields = ['created_at', 'updated_at', 'version']

    def get_queryset(self):
        return DigitalProductGenome.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
