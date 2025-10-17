from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({"status": "ok", "service": "SIMS Backend"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="redoc",
    ),
    path("", include("sims_backend.admissions.urls")),
    path("", include("sims_backend.academics.urls")),
    path("", include("sims_backend.enrollment.urls")),
    path("", include("sims_backend.attendance.urls")),
    path("", include("sims_backend.assessments.urls")),
    path("", include("sims_backend.results.urls")),
    path("", include("sims_backend.requests.urls")),
    path("", include("sims_backend.transcripts.urls")),
]
