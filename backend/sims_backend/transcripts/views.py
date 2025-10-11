from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VerifyTranscriptView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"error": "Transcript verification is not yet implemented."},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )