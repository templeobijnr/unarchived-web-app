from django.http import JsonResponse
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from files.models import UploadedFile
from agentcore.tools import dpg_builder_tool
from .models import DigitalProductGenome
from .serializers import DigitalProductGenomeSerializer
import tempfile
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account


from PIL import Image
import pytesseract
from io import BytesIO

class GenerateDPGFromPromptAndImage(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        image = request.data.get('image')

        if not prompt or not image:
            return Response({"error": "Both prompt and image are required"}, status=400)

        try:
            image = Image.open(BytesIO(image.read()))
            ocr_text = pytesseract.image_to_string(image)
        except Exception as e:
            return Response({"error": f"OCR failed: {str(e)}"}, status=500)

        # Combine prompt + OCR text
        full_prompt = f"{prompt}\n\nImage text:\n{ocr_text}"

        dpg_data = dpg_builder_tool.invoke(full_prompt)

        dpg = DigitalProductGenome.objects.create(
            title=dpg_data.get("title"),
            version=dpg_data.get("version", "1.0"),
            summary=dpg_data["data"].get("summary", ""),  # ✅ Save summary outside
            data={k: v for k, v in dpg_data["data"].items() if k != "summary"},  # ✅ Remove summary from data
            stage=dpg_data.get("stage", "created"),
            owner=request.user
        )
        return Response(DigitalProductGenomeSerializer(dpg).data, status=201)
    
    
class ExportDPG(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            dpg = DigitalProductGenome.objects.get(pk=pk, owner=request.user)
            return JsonResponse({
                "title": dpg.title,
                "version": dpg.version,
                "stage": dpg.stage,
                "data": dpg.data,
                "owner_id": dpg.owner.id,
                "created_at": dpg.created_at.isoformat(),
                "updated_at": dpg.updated_at.isoformat(),
            }, json_dumps_params={'indent': 4})
        except DigitalProductGenome.DoesNotExist:
            return JsonResponse({"error": "DPG not found"}, status=404)