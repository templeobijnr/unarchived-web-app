from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet

router = DefaultRouter()
router.register(r'files', UploadedFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]