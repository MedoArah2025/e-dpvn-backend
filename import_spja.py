from activities.models.spja import MiseADispositionSpja
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

# Index 4 = SPJA
DATA = [
    ["CP/AEROPORT", None, None, None, None, None, None],
    ["CP/BOUKOKI", None, None, None, None, None, None],
    ["CP/FRANCOPHONIE", None, None, None, None, None, None],
    ["CP/KIRKISSOYE", None, None, None, None, None, None],
    ["CP/KOUBIA", None, None, None, None, None, None],
    ["CP/RIVE DROITE", None, None, None, None, None, None],
    ["CP/ROUTE KOLLO", None, None, None, None, None, None],
    ["CP/TALLADJE", None, None, None, None, None, None],
    ["CP/YANTALA", None, None, None, None, None, None],
    ["CSP/ G MARCHE", None, None, None, 32, None, None],
    ["CSP/STADE", None, None, None, 10, None, None],
    ["CSP/WADATA", None, None, None, 25, None, None],
    ["PP/MARCHE BONKANEY", None, None, None, 6, None, None],
    ["PP/PETIT MARCHE", None, None, None, 91, None, None],
    ["SPJA/CCN", None, None, None, None, None, None],
]

DATE = "2025-04-30"
OBJET = "Mise à disposition SPJA"

compteur = 0

for row in DATA:
    code, _, _, _, spja, _, _ = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    if spja not in (None, 0):
        MiseADispositionSpja.objects.create(
            unite=unite,
            date_mise=DATE,
            objet=OBJET,
            nbre_personnes=spja,
            observation=""
        )
        compteur += 1

print(f"{compteur} mises à disposition SPJA importées.")
