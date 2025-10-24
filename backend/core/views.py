"""Custom views for authentication."""
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that accepts email instead of username.

    This view uses the EmailTokenObtainPairSerializer to allow
    users to authenticate using their email address.
    """

    serializer_class = EmailTokenObtainPairSerializer  # type: ignore[assignment]
