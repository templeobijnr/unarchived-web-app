from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from chat.models import Message, Conversation

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