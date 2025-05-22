import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

@pytest.fixture
def admin_client(db):
    admin = User.objects.create_superuser("admin", "a@b.com", "pass")
    c = APIClient()
    c.login(username="admin", password="pass")
    return c

@pytest.mark.django_db
def test_user_list(admin_client):
    url = reverse("user-list")
    resp = admin_client.get(url)
    assert resp.status_code == 200
