from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AIChatViewSet

router = DefaultRouter()
router.register(r'chat', AIChatViewSet, basename='ai-chat')

urlpatterns = [
    path("", include(router.urls)),
]
