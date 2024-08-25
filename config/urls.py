from django.contrib import admin
from external.swagger import (
    SpectacularSwaggerView,
    SpectacularAPIView,
    SpectacularRedocView,
)

from config import settings
from django.urls import path, include
from django.conf.urls.static import static

from renderer.views import render_index_page

swagger_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger_ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = [
    path("", render_index_page, name="home_page"),
    path("admin/", admin.site.urls),
    path("user/v1/", include("apps.user.urls.urls_v1")),
    path("authentication/v1/", include("apps.authentication.urls.urls_v1")),
    path("password/v1/", include("apps.password_management.urls.urls_v1")),
    path("restaurant/v1/", include("apps.restaurant.urls.urls_v1")),
] + swagger_urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
