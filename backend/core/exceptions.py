from typing import Any

from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    response = drf_exception_handler(exc, context)
    if response is None:
        return Response(
            {
                "error": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error",
                    "details": {},
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    data = response.data
    message = data.get("detail") if isinstance(data, dict) else "Request failed"
    return Response(
        {
            "error": {
                "code": response.status_code,
                "message": force_str(message),
                "details": data if isinstance(data, dict) else {"detail": data},
            }
        },
        status=response.status_code,
    )
