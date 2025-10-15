from django.urls import path

from .views import verify_transcript

urlpatterns = [
    path(
        "api/transcripts/verify/<str:token>",
        verify_transcript,
        name="verify-transcript",
    )
]
