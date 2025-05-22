# units/tests/test_models.py

import pytest
from django.db import IntegrityError
from units.models import Unite, ActivityGroup, UniteActivityGroup

@pytest.mark.django_db
def test_unite_str():
    u = Unite.objects.create(nom="TestUnit", type="cp")
    assert str(u) == "TestUnit (Commissariat de Police)"

@pytest.mark.django_db
def test_activitygroup_str():
    g = ActivityGroup.objects.create(nom="Group1", categorie="administratif")
    assert str(g) == "Group1 [Administratif]"

@pytest.mark.django_db
def test_pivot_str_and_uniqueness():
    u = Unite.objects.create(nom="U1", type="cp")
    g = ActivityGroup.objects.create(nom="G1", categorie="administratif")
    uag = UniteActivityGroup.objects.create(unite=u, group=g)
    assert str(uag) == "U1 → G1"
    # Attempting to create a duplicate pivot should raise IntegrityError
    with pytest.raises(IntegrityError):
        UniteActivityGroup.objects.create(unite=u, group=g)
