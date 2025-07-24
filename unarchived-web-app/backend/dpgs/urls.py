
from django.urls import path
from .views import GenerateDPGFromPromptAndImage,ExportDPG,dpg_testing_ui

urlpatterns = [
    path("generate_from_prompt_and_image/", GenerateDPGFromPromptAndImage.as_view()),
    path("export/<int:pk>/", ExportDPG.as_view()),
    path('dpg-test/', dpg_testing_ui, name='dpg_testing_ui'),
    
]
