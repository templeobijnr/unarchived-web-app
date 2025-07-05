
from rest_framework import viewsets, permissions
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from .tasks import run_ocr_on_file

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        run_ocr_on_file.delay(instance.id)
