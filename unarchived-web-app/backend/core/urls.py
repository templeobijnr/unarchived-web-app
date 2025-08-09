"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.middleware.csrf import get_token
from django.urls import path, include
from rest_framework.views import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET'])
def csrf(request):
    return Response({'csrfToken': get_token(request)})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include(('users.urls', 'users'), namespace='users')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/rfq/', include('rfq.urls')),
    path('api/quotes/', include('quotes.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/projects/', include('projects.urls')),
    path('test/', include('test.urls')),
    path("api/", include("files.urls")),
    path('api/ai/', include('agentcore.urls')),
    path('api/dpgs/', include('dpgs.urls')), 
    path('api/csrf/', csrf, name='csrf'),

]


if settings.DEBUG:
    # Serve favicon in development
    from django.views.generic import RedirectView
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(
            url=settings.STATIC_URL + 'favicon.ico', permanent=False)),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)