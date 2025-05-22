import pytest
from django.db import IntegrityError
from units.models import Unite, ActivityGroup
from activities.models.base import BaseActivity
from activities.models.administratif import AutresDeclarations
from activities.models.judiciaire import Infraction
from activities.models.rh import EffectifRH
from activities.models.constat import AccidentCirculation

@pytest.mark.django_db
def test_autres_declarations_str_and_defaults():
    u = Unite.objects.create(nom="U1", type="cp")
    ad = AutresDeclarations.objects.create(
        unite=u,
        date_declaration="2025-05-14",
        type_declaration="Véhicule"
    )
    assert str(ad) == "U1 – Véhicule (En cours)"
    # default brouillon True
    assert ad.brouillon is True

@pytest.mark.django_db
def test_infraction_str_and_fields():
    u = Unite.objects.create(nom="U2", type="cp")
    inf = Infraction.objects.create(
        unite=u,
        date_infraction="2025-05-14",
        categorie_infraction="Vols (tous genre)",
        victime_homme=2,
        victime_femme=1
    )
    assert "Vols (tous genre)" in str(inf)
    assert inf.victime_homme == 2
    assert inf.victime_femme == 1

@pytest.mark.django_db
def test_effectif_rh_requires_date():
    u = Unite.objects.create(nom="U3", type="cp")
    with pytest.raises(IntegrityError):
        # date_rapport est requis et ne peut pas être NULL
        EffectifRH.objects.create(unite=u)

@pytest.mark.django_db
def test_accident_circulation_str_and_ordering():
    u = Unite.objects.create(nom="U4", type="cp")
    a1 = AccidentCirculation.objects.create(
        unite=u,
        date="2025-01-01",
        blesses_graves=1
    )
    a2 = AccidentCirculation.objects.create(
        unite=u,
        date="2025-02-01",
        blesses_graves=0
    )
    # __str__
    assert str(a1) == "U4 – Accident du 2025-01-01"
    # ordering: newest first
    qs = AccidentCirculation.objects.filter(unite=u)
    assert list(qs)[0] == a2
