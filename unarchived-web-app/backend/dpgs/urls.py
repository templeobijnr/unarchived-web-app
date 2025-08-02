# dpgs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DigitalProductGenomeViewSet, UniversalGenerateDPG, ExportDPG

# Set up the router for the DigitalProductGenome API viewsets
router = DefaultRouter()
router.register(r'dpgs', DigitalProductGenomeViewSet)

urlpatterns = [
    # DPG API Endpoints
    path('', include(router.urls)),  # Includes all standard CRUD operations for DigitalProductGenome

    # Custom DPG actions
    path('generate-dpg/', UniversalGenerateDPG.as_view(), name='generate-dpg'),  # DPG generation endpoint
    path('dpgs/<int:pk>/export/', ExportDPG.as_view(), name='export-dpg'),  # Export DPG as JSON
    path('dpgs/<int:pk>/enhance-apparel/', DigitalProductGenomeViewSet.as_view({'post': 'enhance_apparel'}), name='enhance-apparel'),  # Enhance apparel specialization
    path('dpgs/<int:pk>/create-live-spec/', DigitalProductGenomeViewSet.as_view({'post': 'create_live_spec'}), name='create-live-spec'),  # Create shareable live spec
    path('dpgs/<int:pk>/manufacturing-analysis/', DigitalProductGenomeViewSet.as_view({'get': 'manufacturing_analysis'}), name='manufacturing-analysis'),  # Get manufacturability insights
]
