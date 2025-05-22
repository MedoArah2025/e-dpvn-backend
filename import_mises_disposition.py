from activities.models import (
    MiseslctCto, MiseDispositionOcrit, MiseDPMF, MiseDST, MiseDPJ
)
from units.models import Unite

MAPPING = {
    "CP/AEROPORT": "AEROPORT",
    "CP/BOUKOKI": "BOUKOKI",
    "CP/FRANCOPHONIE": "FRANCOPHONIE",
    "CP/KIRKISSOYE": "KIRKISSOYE",
    "CP/KOUBIA": "KOUBIA",
    "CP/RIVE DROITE": "RIVE DROITE",
    "CP/ROUTE KOLLO": "ROUTE KOLLO",
    "CP/TALLADJE": "TALLADJE",
    "CP/YANTALA": "YANTALA",
    "CSP/ G MARCHE": "GRAND MARCHE",
    "CSP/STADE": "STADE",
    "CSP/WADATA": "WADATA",
    "PP/MARCHE BONKANEY": "MARCHE BONKANEY",
    "PP/PETIT MARCHE": "PETIT MARCHE",
    "SPJA/CCN": "SPJA CCN",
}

# ["Unité", SLCT/CTO, OCRTIS, DPMF, SPJA (supprimé), DST, DPJ]
DATA = [
    ["CP/AEROPORT", 2, 5, 7, None, 8, 7],
    ["CP/BOUKOKI", None, 37, None, None, None, None],
    ["CP/FRANCOPHONIE", None, 6, None, None, 5, None],
    ["CP/KIRKISSOYE", 1, None, None, None, 1, None],
    ["CP/KOUBIA", None, 2, 1, None, None, 1],
    ["CP/RIVE DROITE", 2, 10, None, None, None, None],
    ["CP/ROUTE KOLLO", None, 5, 1, None, None, 1],
    ["CP/TALLADJE", 0, 2, 0, None, 0, 0],
    ["CP/YANTALA", 10, None, None, None, None, None],
    ["CSP/ G MARCHE", None, None, 4, None, None, 4],
    ["CSP/STADE", None, None, 4, None, None, 4],
    ["CSP/WADATA", None, None, 2, None, None, 2],
    ["PP/MARCHE BONKANEY", None, None, 3, None, None, 3],
    ["PP/PETIT MARCHE", None, None, 3, None, None, 3],
    ["SPJA/CCN", None, 15, None, None, None, None],
]

DATE = "2025-04-30"

compteur = 0

for row in DATA:
    code, slct, ocrit, dpmf, _spja_supprime, dst, dpj = row  # _spja_supprime ignoré
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # SLCT/CTO
    if slct not in (None, 0):
        MiseslctCto.objects.create(
            unite=unite,
            hommes=slct, femmes=0, mineurs=0,
            date_mise=DATE,
        )
        compteur += 1

    # OCRTIS
    if ocrit not in (None, 0):
        MiseDispositionOcrit.objects.create(
            unite=unite,
            hommes=ocrit, femmes=0, mineurs=0,
            date_mise=DATE,
        )
        compteur += 1

    # DPMF
    if dpmf not in (None, 0):
        MiseDPMF.objects.create(
            unite=unite,
            hommes=dpmf, femmes=0, mineurs=0,
            date_mise=DATE,
        )
        compteur += 1

    # DST
    if dst not in (None, 0):
        MiseDST.objects.create(
            unite=unite,
            hommes=dst, femmes=0, mineurs=0,
            date_mise=DATE,
        )
        compteur += 1

    # DPJ
    if dpj not in (None, 0):
        MiseDPJ.objects.create(
            unite=unite,
            hommes=dpj, femmes=0, mineurs=0,
            date_mise=DATE,
        )
        compteur += 1

print(f"{compteur} enregistrements de mises à disposition importés.")
