from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]