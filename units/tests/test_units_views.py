# units/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from units.models import Unite
from accounts.models import User

@pytest.fixture
def admin_client(db):
    admin = User.objects.create_superuser("admin", "a@b.com", "pass")
    client = APIClient()
    client.login(username="admin", password="pass")
    return client

@pytest.fixture
def sample_unite(db):
    return Unite.objects.create(nom="SampleUnit", type="cp")

@pytest.mark.django_db
def test_list_units_empty(admin_client):
    url = reverse("unit-list")
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_create_unit(admin_client):
    url = reverse("unit-list")
    data = {"nom": "NewUnit", "type": "pp", "parent": None}
    resp = admin_client.post(url, data, format="json")
    assert resp.status_code == 201
    body = resp.json()
    assert body["nom"] == "NewUnit"
    assert body["type"] == "pp"

@pytest.mark.django_db
def test_update_unit(admin_client, sample_unite):
    url = reverse("unit-detail", args=[sample_unite.id])
    resp = admin_client.patch(url, {"nom": "UpdatedUnit"}, format="json")
    assert resp.status_code == 200
    sample_unite.refresh_from_db()
    assert sample_unite.nom == "UpdatedUnit"

@pytest.mark.django_db
def test_delete_unit(admin_client, sample_unite):
    url = reverse("unit-detail", args=[sample_unite.id])
    resp = admin_client.delete(url)
    assert resp.status_code == 204
    assert not Unite.objects.filter(id=sample_unite.id).exists()
