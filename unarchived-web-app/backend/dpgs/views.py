from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from .models import DigitalProductGenome
from .serializers import DigitalProductGenomeSerializer
import tempfile
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import pytesseract
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dpgs.models import DigitalProductGenome
from dpgs.serializers import DigitalProductGenomeSerializer
from agentcore.tools import dpg_builder_tool
from PIL import Image
from io import BytesIO
from files.models import UploadedFile
import os
import fitz  # PyMuPDF
import docx
import csv
import pandas as pd
from django.shortcuts import render



class BearerTokenMixin:
    """
    Mixin to handle Bearer token authentication
    """
    def authenticate_bearer_token(self, request):
        """
        Extract and validate Bearer token from Authorization header
        Returns True if valid, False otherwise
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return False
            
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else ''
        
        # Add your token validation logic here
        # For example, check against database, JWT validation, etc.
        
        # Simple example - replace with your actual validation
        VALID_TOKENS = [
            'your-secret-token-here',
            'test-token-123',
            # Add your valid tokens here
        ]
        
        return token in VALID_TOKENS
    
    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to check authentication before processing
        """
        """if not self.authenticate_bearer_token(request):
            return JsonResponse({
                'error': 'Invalid or missing Bearer token'
            }, status=401)
        
        return super().dispatch(request, *args, **kwargs)"""

class UniversalGenerateDPG(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get("prompt", "")
        file = request.data.get("file")

        extracted_text = ""

        if file:
            file_type = file.content_type
            file_name = file.name.lower()

            if file_type.startswith("image/"):
                image = Image.open(BytesIO(file.read()))
                extracted_text = pytesseract.image_to_string(image)
            elif file_name.endswith(".pdf"):
                pdf = fitz.open(stream=file.read(), filetype="pdf")
                for page in pdf:
                    extracted_text += page.get_text()
            elif file_name.endswith(".xls") or file_name.endswith(".xlsx"):
                try:
                    df = pd.read_excel(file, engine="openpyxl" if file_name.endswith(".xlsx") else "xlrd")
                    extracted_text = df.to_string(index=False)
                except Exception as e:
                    return Response({"error": f"Failed to read Excel file: {str(e)}"}, status=400)
            elif file_name.endswith(".docx"):
                doc = docx.Document(BytesIO(file.read()))
                extracted_text = "\n".join([para.text for para in doc.paragraphs])
            elif file_name.endswith(".txt") or file.content_type == "text/plain":
                extracted_text = file.read().decode("utf-8")
            elif file_name.endswith(".csv"):
                text = file.read().decode("utf-8")
                reader = csv.reader(text.splitlines())
                extracted_text = "\n".join(["\t".join(row) for row in reader])
            else:
                return Response({"error": "Unsupported file type."}, status=400)

        combined_input = f"{prompt}\n\n{extracted_text}".strip()

        try:
            dpg_data = dpg_builder_tool.invoke(combined_input)
            dpg = DigitalProductGenome.objects.create(
                title=dpg_data.get("title"),
                version=dpg_data.get("version", "1.0"),
                summary=dpg_data["data"].pop("summary", ""),
                data=dpg_data.get("data", {}),
                stage=dpg_data.get("stage", "created"),
                owner=request.user
            )
            return Response(DigitalProductGenomeSerializer(dpg).data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


def dpg_testing_ui(request):
    """
    Render the DPG testing UI template
    """
    return render(request, 'dpg_testing_ui.html')




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