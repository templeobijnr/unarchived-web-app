from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, SupplierContactViewSet, CommunicationLogViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'supplier-contacts', SupplierContactViewSet)
router.register(r'communications', CommunicationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]