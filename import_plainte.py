from activities.models import Plainte
from units.models import Unite

MAPPING = {
    "CP/AEROPORT": "AEROPORT",
    "CP/BOUKOKI": "BOUKOKI",
    "CP/FRANCOPHONIE": "FRANCOPHONIE",
    "CP/KIRKISSOYE": "KIRKISSOYE",
    "CP/KOUBIA": "KOUBIA",
    "CP/NIAMEY 2000": "NIAMEY 2000",
    "CP/RIVE DROITE": "RIVE DROITE",
    "CP/ROUTE KOLLO": "ROUTE KOLLO",
    "CP/TALLADJE": "TALLADJE",
    "CP/YANTALA": "YANTALA",
    "CSP/ G MARCHE": "GRAND MARCHE",
    "CSP/STADE": "STADE",
    "CSP/WADATA": "WADATA",
    "PP/MARCHE BONKANEY": "MARCHE BONKANEY",
    "SPJA/CCN": "SPJA/CCN",
}

DATE = "2025-04-30"

DATA = [
    # [Unité, Nombre de dépôts de plainte]
    ["CP/AEROPORT", 25],
    ["CP/BOUKOKI", 60],
    ["CP/FRANCOPHONIE", 21],
    ["CP/KIRKISSOYE", 7],
    ["CP/KOUBIA", 22],
    ["CP/NIAMEY 2000", 33],
    ["CP/RIVE DROITE", 18],
    ["CP/ROUTE KOLLO", 21],
    ["CP/TALLADJE", 40],
    ["CP/YANTALA", 30],
    ["CSP/ G MARCHE", 17],
    ["CSP/STADE", 3],
    ["CSP/WADATA", 4],
    ["PP/MARCHE BONKANEY", 24],
    ["SPJA/CCN", 219],
]

nb_plainte = 0

for row in DATA:
    code, nb = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Vérifie s'il existe déjà une ligne pour cette unité/date
    if not Plainte.objects.filter(
        unite=unite,
        date_plainte=DATE
    ).exists():
        Plainte.objects.create(
            unite=unite,
            date_plainte=DATE,
            nombre_plainte=nb
        )
        nb_plainte += 1

print(f"{nb_plainte} plaintes importées.")
