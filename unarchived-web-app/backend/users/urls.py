from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    
    # ✅ Add this for login
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
