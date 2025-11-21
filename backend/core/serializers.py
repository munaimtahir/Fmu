"""Custom serializers for authentication."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    A custom token obtain pair serializer that uses email instead of username.

    This serializer extends the `TokenObtainPairSerializer` to allow users to
    authenticate using their email address and password. It validates the
    credentials and, if successful, returns a pair of JWT access and refresh
    tokens.
    """

    username_field = "email"

    def validate(self, attrs):
        """
        Validates the user's credentials and generates JWT tokens.

        This method overrides the default validation to authenticate a user
        based on their email and password. It checks for the existence of the
        user, verifies the password, and ensures the user is active. If all
        checks pass, it updates the last login time and returns the tokens.

        Args:
            attrs (dict): The dictionary of input data, expected to contain
                          'email' and 'password'.

        Returns:
            dict: A dictionary containing the 'refresh' and 'access' tokens.

        Raises:
            AuthenticationFailed: If the credentials are invalid, the user
                                  does not exist, or is inactive.
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
