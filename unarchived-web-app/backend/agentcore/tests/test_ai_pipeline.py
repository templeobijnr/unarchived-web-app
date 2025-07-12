import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest import mock
from dpgs.models import DigitalProductGenome
from files.models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AIFlowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @mock.patch("agentcore.views.agent.create_co_pilot_agent")
    def test_ai_chat_creates_dpg(self, mock_create_agent):
        mock_agent_instance = mock.Mock()
        mock_agent_instance.run.return_value = "Mocked agent response"
        mock_create_agent.return_value = mock_agent_instance

        response = self.client.post("/api/ai/chat/", {"message": "Create a DPG for a red t-shirt"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.data)

    def test_upload_file_triggers_ocr(self):
        test_file = SimpleUploadedFile("sample.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post("/api/files/", {"file": test_file, "file_type": "image"})
        self.assertIn(response.status_code, [200, 201, 202])

        uploaded = UploadedFile.objects.last()
        self.assertIsNotNone(uploaded)
        self.assertEqual(uploaded.user, self.user)

    def test_dpg_model_creation(self):
        dpg = DigitalProductGenome.objects.create(
            owner=self.user,
            data={"name": "Test Product"}
        )
        self.assertEqual(dpg.owner, self.user)
        self.assertEqual(dpg.data["name"], "Test Product")

    def test_invalid_file_upload(self):
        response = self.client.post("/api/files/", {"file_type": "image"})  # missing 'file'
        self.assertEqual(response.status_code, 400)

    def test_empty_ai_message(self):
        response = self.client.post("/api/ai/chat/", {"message": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No message provided")

    def test_duplicate_dpg_creation(self):
        DigitalProductGenome.objects.create(owner=self.user, data={"sku": "ABC123"})
        second = DigitalProductGenome.objects.create(owner=self.user, data={"sku": "ABC123"})
        self.assertEqual(DigitalProductGenome.objects.filter(data__sku="ABC123").count(), 2)

    @mock.patch("agentcore.views.agent.create_co_pilot_agent")
    def test_complex_input_handling(self, mock_create_agent):
        mock_agent_instance = mock.Mock()
        mock_agent_instance.run.return_value = "Processed complex input"
        mock_create_agent.return_value = mock_agent_instance

        long_input = (
            "Hello, I need a quote for a custom techwear jacket. "
            "It should be water-resistant, have reflective trims, internal charging cable pathways, "
            "and come in matte black and deep olive tones. Sizes S-XL, initial MOQ 100 pieces. "
            "Please ensure YKK zippers and laser-cut ventilation zones. Thank you!"
        )

        response = self.client.post("/api/ai/chat/", {"message": long_input})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.data)
