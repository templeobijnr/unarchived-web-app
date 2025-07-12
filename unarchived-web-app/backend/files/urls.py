from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', UploadedFileViewSet)  # empty string = mount directly at /files/

urlpatterns = [
    path('', include(router.urls)),
]
