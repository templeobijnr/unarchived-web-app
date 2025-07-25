from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from chat.models import Message, Conversation
from unittest import mock

User = get_user_model()

class ChatAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass456")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])

    def test_create_message(self):
        url = reverse("message-list")
        data = {
            "author": "user",
            "content": "Hello, AI!",
            "conversation": self.conversation.id,
            "user": self.user1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Hello, AI!")
        self.assertEqual(response.data["author"], "user")

    def test_list_messages_pagination(self):
        url = reverse("message-list")
        for i in range(25):
            Message.objects.create(
                author="user",
                content=f"Msg {i}",
                conversation=self.conversation,
                user=self.user1
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 20)  # Default page size

    def test_filter_messages_by_conversation(self):
        other_convo = Conversation.objects.create()
        other_convo.participants.set([self.user1])
        Message.objects.create(
            author="user",
            content="In other convo",
            conversation=other_convo,
            user=self.user1
        )
        url = reverse("message-list")
        response = self.client.get(url, {"conversation": self.conversation.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for msg in response.data["results"]:
            self.assertEqual(msg["conversation"], self.conversation.id)

    def test_update_message(self):
        msg = Message.objects.create(
            author="user",
            content="Original",
            conversation=self.conversation,
            user=self.user1
        )
        url = reverse("message-detail", args=[msg.id])
        response = self.client.patch(url, {"content": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated")

    def test_delete_message(self):
        msg = Message.objects.create(
            author="user",
            content="To delete",
            conversation=self.conversation,
            user=self.user1
        )
        url = reverse("message-detail", args=[msg.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(id=msg.id).exists())

    def test_cannot_modify_others_message(self):
        msg = Message.objects.create(
            author="user",
            content="Not yours",
            conversation=self.conversation,
            user=self.user2
        )
        url = reverse("message-detail", args=[msg.id])
        response = self.client.patch(url, {"content": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_message_as_read(self):
        msg = Message.objects.create(
            author="ai",
            content="Read me",
            conversation=self.conversation,
            user=self.user1,
            is_read=False
        )
        url = reverse("message-detail", args=[msg.id])
        response = self.client.patch(url, {"is_read": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_read"])

    def test_conversation_list(self):
        url = reverse("conversation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn(self.user1.id, response.data["results"][0]["participants"])

    @mock.patch("agentcore.agent.ConversationalAgent.chat")
    def test_ai_chat_bridge_success(self, mock_agent_chat):
        # Mock agent response
        mock_agent_chat.return_value = {
            "response": "Here is your DPG.",
            "suggestions": ["Next: Generate an RFQ"],
            "context": {"ai_confidence": 0.95, "ai_version": "gpt-4"}
        }
        url = reverse("message-ai-chat")
        data = {
            "conversation": self.conversation.id,
            "content": "Can you help me create a DPG for a blue backpack?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("ai_message", response.data)
        self.assertIn("user_message", response.data)
        self.assertIn("suggestions", response.data)
        self.assertIn("context", response.data)
        # Check AI metadata
        self.assertEqual(response.data["ai_message"]["ai_confidence"], 0.95)
        self.assertEqual(response.data["ai_message"]["ai_version"], "gpt-4")
        # Check conversation linking
        self.assertEqual(response.data["user_message"]["conversation"], self.conversation.id)
        self.assertEqual(response.data["ai_message"]["conversation"], self.conversation.id)

    def test_ai_chat_bridge_invalid_conversation(self):
        url = reverse("message-ai-chat")
        data = {
            "conversation": 9999,  # Non-existent
            "content": "Test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)

    def test_ai_chat_bridge_security(self):
        # Create a conversation user1 is NOT a participant of
        convo = Conversation.objects.create()
        convo.participants.set([self.user2])
        url = reverse("message-ai-chat")
        data = {
            "conversation": convo.id,
            "content": "Should not work"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)