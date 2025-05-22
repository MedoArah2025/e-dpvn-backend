from activities.models import Cin
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
    # [Unité, CARTE ETABLIES, CARTE RENOUVELLEES, CARTE DUPLICATA, Total]
    ["CP/AEROPORT", 837, 271, 64, 1172],
    ["CP/BOUKOKI", 1081, 327, 55, 1463],
    ["CP/FRANCOPHONIE", 2230, 606, 58, 2894],
    ["CP/KIRKISSOYE", 632, 215, 127, 974],
    ["CP/KOUBIA", 1528, 274, 106, 1908],
    ["CP/NIAMEY 2000", 906, 102, 65, 1073],
    ["CP/RIVE DROITE", 1074, 429, 161, 1664],
    ["CP/ROUTE KOLLO", 329, 0, 0, 329],
    ["CP/TALLADJE", 1226, 374, 49, 1649],
    ["CP/YANTALA", 1144, 299, 131, 1574],
    ["CSP/ G MARCHE", 1346, 0, 78, 1424],
    ["CSP/STADE", 788, 0, 2, 790],
    ["CSP/WADATA", 2327, 365, 105, 2797],
    ["PP/MARCHE BONKANEY", 1426, 175, 68, 1669],
    ["PP/PETIT MARCHE", 707, 0, 44, 751],
    ["SPJA/CCN", 1174, 372, 64, 1610],
]

nb_cin = 0

for row in DATA:
    code, etablies, renouvellees, duplicata, total = row
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
    if not Cin.objects.filter(
        unite=unite,
        date_etablissement=DATE
    ).exists():
        Cin.objects.create(
            unite=unite,
            date_etablissement=DATE,
            carte_etablie=etablies or 0,
            carte_reprise=renouvellees or 0,
            duplicata=duplicata or 0
        )
        nb_cin += 1

print(f"{nb_cin} CIN importées.")
