from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_transcript(request, token: str):
    return Response(
        {
            "error": {
                "code": 501,
                "message": "Not Implemented",
                "details": {"token": token},
            }
        },
        status=501,
    )
