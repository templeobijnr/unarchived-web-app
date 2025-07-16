from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, DashboardViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'', ProjectViewSet, basename='projects')
router.register(r'kpis', KPIViewSet)


urlpatterns = [
    path('', include(router.urls)),
]