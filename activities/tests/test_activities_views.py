import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from units.models import Unite
from activities.models.judiciaire import Infraction

@pytest.fixture
def admin_client(db):
    admin = User.objects.create_superuser("admin", "a@b.com", "pass")
    c = APIClient()
    c.login(username="admin", password="pass")
    return c

@pytest.fixture
def sample_unite(db):
    return Unite.objects.create(nom="TestUnit", type="cp")

@pytest.mark.django_db
def test_list_infractions_empty(admin_client):
    url = reverse("infractions-list")  # basename='infractions'
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_create_and_retrieve_infraction(admin_client, sample_unite):
    url = reverse("infractions-list")
    data = {
        "unite": sample_unite.id,
        "date_infraction": "2025-05-14",
        "categorie_infraction": "Vols (tous genre)",
        "victime_homme": 1,
        "victime_femme": 0,
        "victime_mineur": 0
    }
    # POST
    resp = admin_client.post(url, data, format="json")
    assert resp.status_code == 201
    pk = resp.json()["id"]

    # GET detail
    detail_url = reverse("infractions-detail", args=[pk])
    resp2 = admin_client.get(detail_url)
    assert resp2.status_code == 200
    body = resp2.json()
    assert body["categorie_infraction"] == data["categorie_infraction"]
    assert body["victime_homme"] == 1

@pytest.mark.django_db
def test_update_infraction(admin_client, sample_unite):
    # create first
    inf = Infraction.objects.create(
        unite=sample_unite,
        date_infraction="2025-05-14",
        categorie_infraction="Vols (tous genre)",
    )
    url = reverse("infractions-detail", args=[inf.id])
    resp = admin_client.patch(url, {"victime_femme": 2}, format="json")
    assert resp.status_code == 200
    assert Infraction.objects.get(id=inf.id).victime_femme == 2

@pytest.mark.django_db
def test_delete_infraction(admin_client, sample_unite):
    inf = Infraction.objects.create(
        unite=sample_unite,
        date_infraction="2025-05-14",
        categorie_infraction="Vols (tous genre)",
    )
    url = reverse("infractions-detail", args=[inf.id])
    resp = admin_client.delete(url)
    assert resp.status_code == 204
    assert not Infraction.objects.filter(id=inf.id).exists()
