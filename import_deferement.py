from activities.models import Deferement
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
    "SPJA/CCN": "SPJA/CCN",
}

DATE = "2025-04-30"

DATA = [
    # [Unité, Nombre de personnes déférées]
    ["CP/AEROPORT", 64],
    ["CP/BOUKOKI", 71],
    ["CP/FRANCOPHONIE", 137],
    ["CP/KIRKISSOYE", 14],
    ["CP/KOUBIA", 74],
    ["CP/NIAMEY 2000", 32],
    ["CP/RIVE DROITE", 49],
    ["CP/ROUTE KOLLO", 5],
    ["CP/TALLADJE", 66],
    ["CP/YANTALA", 32],
    ["SPJA/CCN", 103],
]

nb_deferement = 0

for row in DATA:
    code, nb_deferes = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Vérifie s'il existe déjà une ligne pour cette unité/date/catégorie
    if not Deferement.objects.filter(
        unite=unite,
        date_interpellation=DATE,
        categorie_infraction="TOTAL"
    ).exists():
        Deferement.objects.create(
            unite=unite,
            date_interpellation=DATE,
            categorie_infraction="TOTAL",
            nombre_deferement=nb_deferes
        )
        nb_deferement += 1

print(f"{nb_deferement} défèrement(s) importé(s).")
