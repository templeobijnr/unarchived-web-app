
from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard
    path('', views.TestingDashboardView.as_view(), name='testing_dashboard'),
    path('html/', views.testing_dashboard_html, name='testing_dashboard_html'),
    
    # Component testing endpoints
    path('users/', views.UserTestingView.as_view(), name='user_testing'),
    path('dpgs/', views.DPGTestingView.as_view(), name='dpg_testing'),
    path('agent/', views.AgentTestingView.as_view(), name='agent_testing'),
    path('analysis/', views.AnalysisTestingView.as_view(), name='analysis_testing'),
    path('knowledge/', views.KnowledgeTestingView.as_view(), name='knowledge_testing'),
    path('suppliers/', views.SupplierTestingView.as_view(), name='supplier_testing'),
    path('files/', views.FileTestingView.as_view(), name='file_testing'),
    
    # Legacy OCR test
    #path('ocr/', views.TestVisionOCRView.as_view(), name='test_ocr'),
]
