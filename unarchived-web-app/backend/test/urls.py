
from django.urls import path
from .views import TestVisionOCRView

urlpatterns = [
    path('ocr-test/', TestVisionOCRView.as_view(), name='ocr-test'),
]
