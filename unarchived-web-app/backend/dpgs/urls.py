
from django.urls import path
from .views import GenerateDPGFromPromptAndImage

urlpatterns = [
    path("generate_from_prompt_and_image/", GenerateDPGFromPromptAndImage.as_view()),
]
