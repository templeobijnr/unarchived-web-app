from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DigitalProductGenomeViewSet

router = DefaultRouter()
router.register(r'dpgs', DigitalProductGenomeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]