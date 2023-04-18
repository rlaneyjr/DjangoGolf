"""
Tests for the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

USER_URL = reverse("core:create")


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


# class PrivateUserAPITests(TestCase):
#     pass
