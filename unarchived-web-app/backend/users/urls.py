from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, CustomTokenObtainPairView, ActivateAccountView, projectmgt_ui

app_name = 'users'

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    
    # ✅ Add this for login
    
    path("mgt/", projectmgt_ui, name="projectmgt_ui"),
    
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),

]
