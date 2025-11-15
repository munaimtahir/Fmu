"""Custom serializers for authentication."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer that accepts email instead of username.

    This allows users to authenticate using their email address and password,
    which is more user-friendly than using a username.
    """

    username_field = "email"

    def validate(self, attrs):
        """
        Validate the credentials and return tokens.

        This method overrides the parent to:
        1. Accept 'email' instead of 'username'
        2. Look up the user by email
        3. Validate password
        4. Return JWT tokens
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Use generic error message to avoid leaking user information
                raise AuthenticationFailed(
                    "No active account found with the given credentials"
                )

            # Check password
            if not user.check_password(password):
                raise AuthenticationFailed(
                    "No active account found with the given credentials"
                )

            # Check if user is active
            if not user.is_active:
                raise AuthenticationFailed(
                    "No active account found with the given credentials"
                )

            # Update last login
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)

            # Generate tokens
            refresh = self.get_token(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return data
        else:
            raise AuthenticationFailed("Must include 'email' and 'password'.")
