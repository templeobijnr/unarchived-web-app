from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from projects.models import Project, ProjectMember, ProjectUpload, ProjectContextEngine
from .models import UploadedFile
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
import boto3
from .serializers import FileSerializer
from projects.permissions import IsProjectMember
import mimetypes
from rest_framework.exceptions import PermissionDenied
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from projects.analysis import trigger_ai_analysis
from knowledge_base.models import KnowledgeChunk

class ProjectFileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        if not ProjectMember.objects.filter(user=self.request.user, project_id=project_id).exists():
            raise PermissionDenied("You are not a member of this project.")
        return UploadedFile.objects.filter(project__id=project_id).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        files = request.FILES.getlist('file')

        if not files:
            return Response({"detail": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded = []
        for file in files:
            mime_type, _ = mimetypes.guess_type(file.name)
            serializer = FileSerializer(data={
                'project': project.pk,
                'file': file,
                'original_filename': file.name,
                'file_type': mime_type or '',
                'size': file.size
            })
            serializer.is_valid(raise_exception=True)
            serializer.save(uploaded_by=request.user)
            file_instance = serializer.instance
            trigger_ai_analysis(file_instance)
            uploaded.append(file_instance.original_filename)

        return Response({'detail': 'File(s) uploaded successfully', 'files':uploaded}, status=status.HTTP_201_CREATED)
            

class FileDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            file = UploadedFile.objects.get(pk=pk)
            file.file.delete(save=False)  # Delete from S3
            file.delete()
            return Response({'detail': 'File deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except UploadedFile.DoesNotExist:
            raise Http404
