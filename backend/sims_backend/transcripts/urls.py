from django.urls import path
from .views import VerifyTranscriptView

urlpatterns = [
    path('verify/', VerifyTranscriptView.as_view(), name='verify-transcript'),
]