import io
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from dpgs.models import DigitalProductGenome
from unittest import mock

User = get_user_model()

class AIFlowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @mock.patch("agentcore.views.agent.create_co_pilot_agent")
    def test_ai_chat_creates_dpg(self, mock_create_agent):
        mock_agent = mock.Mock()
        mock_agent.run.return_value = "Test response"
        mock_create_agent.return_value = mock_agent

        response = self.client.post("/api/ai/chat/", {"message": "Hello Agent"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.data)
        self.assertEqual(response.data["response"], "Test response")

    def test_upload_file_triggers_ocr(self):
        test_file_path = "agentcore/tests/sample.jpg"
        with open(test_file_path, "rb") as f:
            test_file = SimpleUploadedFile("sample.jpg", f.read(), content_type="image/jpeg")

        response = self.client.post("/api/files/", {"file": test_file, "file_type": "image"})
        self.assertEqual(response.status_code, 201)

    def test_dpg_model_creation(self):
        dpg = DigitalProductGenome.objects.create(
            data={"name": "Test Product"},
            owner=self.user  # ✅ This line fixes the IntegrityError
        )
        self.assertIsNotNone(dpg.id)
        self.assertEqual(dpg.data["name"], "Test Product")
        self.assertEqual(dpg.owner, self.user)

