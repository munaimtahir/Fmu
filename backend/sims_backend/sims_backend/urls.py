from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("sims_backend.admissions.urls")),
    path("", include("sims_backend.academics.urls")),
    path("", include("sims_backend.enrollment.urls")),
    path("", include("sims_backend.attendance.urls")),
    path("", include("sims_backend.assessments.urls")),
    path("", include("sims_backend.results.urls")),
    path("", include("sims_backend.transcripts.urls")),
]
