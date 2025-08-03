from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, CustomTokenObtainPairView,login_test_ui,register_user_ui, ActivateAccountView

app_name = 'users'

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    
    # ✅ Add this for login
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logins/", login_test_ui, name="login_test_ui"),
    path('register-ui/', register_user_ui, name='register_user_ui'),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),

]
