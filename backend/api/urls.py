from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# Create router
router = DefaultRouter()
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'supplier-contacts', views.SupplierContactViewSet)
router.register(r'rfqs', views.RFQViewSet)
router.register(r'quotes', views.QuoteViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'kpis', views.KPIViewSet)
router.register(r'communications', views.CommunicationLogViewSet)
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')
router.register(r'auth', views.AuthViewSet, basename='auth')

# URL patterns
urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Authentication (JWT)
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.register_user, name='register_user'),
    
    # Session-based authentication endpoints
    path('auth/session/login/', views.AuthViewSet.as_view({'post': 'login'}), name='session_login'),
    path('auth/session/logout/', views.AuthViewSet.as_view({'post': 'logout'}), name='session_logout'),
    path('auth/session/user/', views.AuthViewSet.as_view({'get': 'user'}), name='session_user'),
    
    # AI Chat
    path('chat/send/', views.MessageViewSet.as_view({'post': 'send_message'}), name='send_message'),
    path('chat/create-rfq/', views.MessageViewSet.as_view({'post': 'create_rfq'}), name='create_rfq'),
    
    # Supplier verification endpoints
    path('suppliers/<int:pk>/verify/', views.SupplierViewSet.as_view({'post': 'verify'}), name='supplier_verify'),
    path('suppliers/<int:pk>/submit-documents/', views.SupplierViewSet.as_view({'post': 'submit_documents'}), name='supplier_submit_documents'),
    path('suppliers/<int:pk>/review/', views.SupplierViewSet.as_view({'post': 'review'}), name='supplier_review'),
    path('suppliers/<int:pk>/contacts/', views.SupplierViewSet.as_view({'get': 'contacts'}), name='supplier_contacts'),
    path('suppliers/<int:pk>/communications/', views.SupplierViewSet.as_view({'get': 'communications'}), name='supplier_communications'),
    path('suppliers/<int:pk>/performance-metrics/', views.SupplierViewSet.as_view({'get': 'performance_metrics'}), name='supplier_performance_metrics'),
    
    # RFQ distribution endpoints
    path('rfqs/<int:pk>/distribute/', views.RFQViewSet.as_view({'post': 'distribute'}), name='rfq_distribute'),
    path('rfqs/<int:pk>/suppliers/', views.RFQViewSet.as_view({'get': 'suppliers'}), name='rfq_suppliers'),
    path('rfqs/<int:pk>/responses/', views.RFQViewSet.as_view({'get': 'responses'}), name='rfq_responses'),
    path('rfqs/<int:pk>/distribution-stats/', views.RFQViewSet.as_view({'get': 'distribution_stats'}), name='rfq_distribution_stats'),
    path('rfqs/<int:pk>/track-view/', views.RFQViewSet.as_view({'post': 'track_view'}), name='rfq_track_view'),
    
    # Quote management endpoints
    path('quotes/<int:pk>/accept/', views.QuoteViewSet.as_view({'post': 'accept'}), name='quote_accept'),
    path('quotes/<int:pk>/reject/', views.QuoteViewSet.as_view({'post': 'reject'}), name='quote_reject'),
] 