from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectStageViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='projects')
router.register(r'stages', ProjectStageViewSet, basename='project-stages')


urlpatterns = [
    path('', include(router.urls)),
]