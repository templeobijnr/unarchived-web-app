
from django.urls import path
from .views import GenerateDPGFromPromptAndImage,ExportDPG

urlpatterns = [
    path("generate_from_prompt_and_image/", GenerateDPGFromPromptAndImage.as_view()),
    path("export/<int:pk>/", ExportDPG.as_view())
]
