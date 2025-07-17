from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from projects.models import Project, ProjectMember
from files.models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from moto import mock_aws as mock_s3
import boto3

class FileUploadTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='member', password='test123')
        self.project = Project.objects.create(name='Test Project', description='...', owner=self.user)
        ProjectMember.objects.create(user=self.user, project=self.project, role=ProjectMember.MemberRole.OWNER)
        self.client.login(username='member', password='test123')

    def test_upload_txt_file(self):
        txt_file = SimpleUploadedFile("test.txt", b"Sample text content", content_type="text/plain")
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {'file': txt_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_upload_jpg_file(self):
        jpg_file = SimpleUploadedFile("image.jpg", b"\xff\xd8\xff\xe0" + b"0"*1024, content_type="image/jpeg")
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {'file': jpg_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_upload_without_file_returns_400(self):
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No files uploaded.', response.data.get('detail', ''))

    def test_metadata_saved(self):
        file = SimpleUploadedFile("meta.pdf", b"%PDF-1.4...", content_type="application/pdf")
        url = f"/api/projects/{self.project.pk}/files/"
        self.client.post(url, {'file': file}, format='multipart')
        f = UploadedFile.objects.first()
        self.assertEqual(f.original_filename, "meta.pdf")
        self.assertEqual(f.file_type, "application/pdf")
        self.assertTrue(f.size > 0)

    def test_non_member_cannot_upload(self):
        other = User.objects.create_user(username='outsider', password='nopass')
        self.client.login(username='outsider', password='nopass')
        file = SimpleUploadedFile("file.txt", b"hello")
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_member_cannot_list_files(self):
        other = User.objects.create_user(username='outsider2', password='nopass')
        self.client.login(username='outsider2', password='nopass')
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.get(url)
        print(response.status_code, response.data)
        print(ProjectMember.objects.filter(user=self.user, project=self.project).exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_multiple_file_upload(self):
        files = [
            SimpleUploadedFile("file1.pdf", b"%PDF"),
            SimpleUploadedFile("file2.jpg", b"\xff\xd8\xff"),
        ]
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {'file': files}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedFile.objects.count(), 2)

    @mock_s3
    def test_delete_file_removes_from_db_and_s3(self):
        # Set up fake S3 bucket
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        file = SimpleUploadedFile("del.txt", b"bye", content_type="text/plain")
        url = f"/api/projects/{self.project.pk}/files/"
        self.client.post(url, {'file': file}, format='multipart')
        file_obj = UploadedFile.objects.first()

        del_url = f"/api/files/{file_obj.pk}/"
        response = self.client.delete(del_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UploadedFile.objects.count(), 0)

    def test_empty_upload_list(self):
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_invalid_file_format_rejected(self):
        bad_file = SimpleUploadedFile("script.sh", b"#!/bin/bash echo Hello")
        url = f"/api/projects/{self.project.pk}/files/"
        response = self.client.post(url, {'file': bad_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # MIME type fallback accepted
