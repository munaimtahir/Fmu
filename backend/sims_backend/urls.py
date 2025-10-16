from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({"status": "ok", "service": "SIMS Backend"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),
    path("", include("sims_backend.admissions.urls")),
    path("", include("sims_backend.academics.urls")),
    path("", include("sims_backend.enrollment.urls")),
    path("", include("sims_backend.attendance.urls")),
    path("", include("sims_backend.assessments.urls")),
    path("", include("sims_backend.results.urls")),
    path("", include("sims_backend.requests.urls")),
    path("", include("sims_backend.transcripts.urls")),
]
