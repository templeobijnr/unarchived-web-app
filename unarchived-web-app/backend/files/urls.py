from rest_framework.routers import DefaultRouter
from .views import ProjectFileViewSet
from django.urls import path, include
from files.views import FileDeleteView
router = DefaultRouter()

urlpatterns = [
    path('projects/<int:project_pk>/files/', ProjectFileViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('files/<int:pk>/', FileDeleteView.as_view()),
]