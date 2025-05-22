from activities.models import DeclarationVol
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
    "PP/PETIT MARCHE": "PETIT MARCHE",
    "SPJA/CCN": "SPJA/CCN",
}

DATE = "2025-04-30"

DATA = [
    ["CP/AEROPORT", 63, 4, 3],
    ["CP/BOUKOKI", 105, 3, 8],
    ["CP/FRANCOPHONIE", 184, 1, 1],
    ["CP/KIRKISSOYE", 72, 2, None],
    ["CP/KOUBIA", 98, None, 1],
    ["CP/NIAMEY 2000", 99, 1, 3],
    ["CP/RIVE DROITE", 116, 1, 3],
    ["CP/ROUTE KOLLO", 18, None, None],
    ["CP/TALLADJE", 104, 0, 7],
    ["CP/YANTALA", 95, None, None],
    ["CSP/ G MARCHE", 44, 4, 1],
    ["CSP/STADE", 24, 1, None],
    ["CSP/WADATA", 63, 1, None],
    ["PP/MARCHE BONKANEY", 62, 3, 1],
    ["PP/PETIT MARCHE", 2, None, 1],
    ["SPJA/CCN", 385, 3, 10],
]

nb_vol = 0
nb_agression = 0
nb_arrache = 0

for row in DATA:
    code, nb_vols, nb_agressions, nb_arrache = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Déclaration vol simple
    if nb_vols not in (None, 0):
        if not DeclarationVol.objects.filter(
            unite=unite, date_plainte=DATE, type_vol="Vol simple"
        ).exists():
            DeclarationVol.objects.create(
                unite=unite,
                date_plainte=DATE,
                type_vol="Vol simple",
                nombre_vol=nb_vols,
                quartier=""
            )
            nb_vol += 1

    # Déclaration agression suivie de vol
    if nb_agressions not in (None, 0):
        if not DeclarationVol.objects.filter(
            unite=unite, date_plainte=DATE, type_vol="Agression suivie de vol"
        ).exists():
            DeclarationVol.objects.create(
                unite=unite,
                date_plainte=DATE,
                type_vol="Agression suivie de vol",
                nombre_vol=nb_agressions,
                quartier=""
            )
            nb_agression += 1

    # Déclaration vol à l'arraché
    if nb_arrache not in (None, 0):
        if not DeclarationVol.objects.filter(
            unite=unite, date_plainte=DATE, type_vol="Vol à l'arraché"
        ).exists():
            DeclarationVol.objects.create(
                unite=unite,
                date_plainte=DATE,
                type_vol="Vol à l'arraché",
                nombre_vol=nb_arrache,
                quartier=""
            )
            nb_arrache += 1

print(f"{nb_vol} vols simples, {nb_agression} agressions suivies de vol, {nb_arrache} vols à l'arraché importés.")
