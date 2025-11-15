"""Tests for email-based authentication."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_with_email():
    """Create a test user with an email address."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    return user


def test_login_with_email_success(user_with_email):
    """Test that users can login with email and password."""
    client = APIClient()

    response = client.post(
        "/api/auth/token/", {"email": "test@example.com", "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


def test_login_with_email_wrong_password(user_with_email):
    """Test that login fails with wrong password."""
    client = APIClient()

    response = client.post(
        "/api/auth/token/", {"email": "test@example.com", "password": "wrongpassword"}
    )

    assert response.status_code == 401


def test_login_with_nonexistent_email():
    """Test that login fails with non-existent email."""
    client = APIClient()

    response = client.post(
        "/api/auth/token/",
        {"email": "nonexistent@example.com", "password": "testpass123"},
    )

    assert response.status_code == 401


def test_login_with_inactive_user(user_with_email):
    """Test that login fails for inactive users."""
    user_with_email.is_active = False
    user_with_email.save()

    client = APIClient()

    response = client.post(
        "/api/auth/token/", {"email": "test@example.com", "password": "testpass123"}
    )

    assert response.status_code == 401


def test_login_missing_email():
    """Test that login fails when email is missing."""
    client = APIClient()

    response = client.post("/api/auth/token/", {"password": "testpass123"})

    assert response.status_code == 400


def test_login_missing_password(user_with_email):
    """Test that login fails when password is missing."""
    client = APIClient()

    response = client.post("/api/auth/token/", {"email": "test@example.com"})

    assert response.status_code == 400


def test_login_empty_credentials():
    """Test that login fails with empty credentials."""
    client = APIClient()

    response = client.post("/api/auth/token/", {})

    assert response.status_code == 400
