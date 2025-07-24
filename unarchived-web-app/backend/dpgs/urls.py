
from django.urls import path
from .views import ExportDPG,dpg_testing_ui

urlpatterns = [
  
    path("export/<int:pk>/", ExportDPG.as_view()),
    path('dpg-test/', dpg_testing_ui, name='dpg_testing_ui'),
    
]
