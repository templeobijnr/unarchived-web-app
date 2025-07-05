from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'kpis', KPIViewSet)
router.register(r'dashboard', DashboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]