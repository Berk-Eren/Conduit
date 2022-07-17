"""conduit_realworld_example_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from apps.user.urls import urlpatterns

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view as yasg_get_schema_view
from drf_yasg import openapi


openapi_schema_view = get_schema_view(
    title="Your Project",
    description="API for all things …",
    version="1.0.0"
)

openapi_yasg_schema_view = yasg_get_schema_view(
    openapi.Info(
        title="Your Project",
        description="API for all things …",
        version="1.0.0",
        default_version="v1"
    ),
    permission_classes = [permissions.AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("apps.articles.urls")),
    path("api/", include("apps.user.urls", namespace="user")),

    path('api/token/', TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('openapi/', openapi_schema_view, name='openapi-schema'),
    path('documentation/drf', TemplateView.as_view(**{
        "template_name": "swagger-ui.html",
        "extra_context": {'schema_url':'openapi-schema'}
    }), name="swagger-ui"),
    path('documentation/swagger-ui', openapi_yasg_schema_view.with_ui("swagger")),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)