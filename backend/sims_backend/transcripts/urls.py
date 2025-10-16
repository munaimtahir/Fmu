from django.urls import path

from .views import get_transcript, verify_transcript

urlpatterns = [
    path(
        "api/transcripts/<int:student_id>/", get_transcript, name="get-transcript"
    ),
    path(
        "api/transcripts/verify/<str:token>/",
        verify_transcript,
        name="verify-transcript",
    ),
]
