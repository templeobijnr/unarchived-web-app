from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

router.register(r'kpis', KPIViewSet)


urlpatterns = [
    path('', include(router.urls)),
]