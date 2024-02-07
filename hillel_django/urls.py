"""hillel_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from telegram.views import accept_telegram_message

from products.views import registration_view, github_user_view, profile_view
from products.viewsets import ProductViewSet, CategoryViewSet, OrderViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("orders", OrderViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Store API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", obtain_auth_token),
    path("api/register/", registration_view),
    path("api/", include(router.urls)),
    path("telegram/", accept_telegram_message),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include("allauth.urls")),
    path("logout", LogoutView.as_view()),
    path("github", github_user_view),
    path('profile/', profile_view, name='profile'),
]
