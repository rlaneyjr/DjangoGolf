"""
Tests for the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

USER_URL = reverse("core:create")
TOKEN_URL = reverse("core:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test public features of the user api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_works(self):
        """Test creating a user works"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_email_exists_fails(self):
        """Test if we can create a user with an email that's already used"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        create_user(**payload)
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_fails(self):
        """Test that we can't create a user with a short password"""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "first_name": "First",
            "last_name": "Last",
        }

        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user_works(self):
        """Test generates token for valid credentials"""
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"], "password": user_details["password"]}
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_bad_credentials_fails(self):
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"], "password": "bad-password"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


# class PrivateUserAPITests(TestCase):
#     pass
