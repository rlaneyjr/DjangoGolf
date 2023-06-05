import pytest
from django.shortcuts import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_unauth_create_player_fails():
    client = APIClient()
    player_endpoint = reverse("home:players-list")
    data = {
        "name": "Test Player"
    }

    res = client.post(player_endpoint, data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
