from activities.models import PersonnesInterpelle, Gav
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
    # [Unité, Nombre interpellés, Nombre GAV]
    ["CP/AEROPORT", 9, 26],
    ["CP/BOUKOKI", 475, 491],
    ["CP/FRANCOPHONIE", 73, 71],
    ["CP/KIRKISSOYE", 4, 55],
    ["CP/KOUBIA", 65, 65],
    ["CP/NIAMEY 2000", 476, 104],
    ["CP/RIVE DROITE", 46, 61],
    ["CP/ROUTE KOLLO", 9, 17],
    ["CP/TALLADJE", 82, 130],
    ["CP/YANTALA", 50, 50],
    ["CSP/ G MARCHE", 35, None],
    ["CSP/STADE", 9, None],
    ["CSP/WADATA", 26, None],
    ["PP/MARCHE BONKANEY", None, None],
    ["PP/PETIT MARCHE", 139, None],
    ["SPJA/CCN", 35, 181],
]

nb_interpelle = 0
nb_gav = 0

for row in DATA:
    code, interpelle, gav = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Personnes interpellées (anti-doublon)
    if interpelle not in (None, 0):
        if not PersonnesInterpelle.objects.filter(
            unite=unite, date_interpellation=DATE, categorie_infraction="TOTAL"
        ).exists():
            PersonnesInterpelle.objects.create(
                unite=unite,
                date_interpellation=DATE,
                categorie_infraction="TOTAL",
                nombre_pers_interp=interpelle
            )
            nb_interpelle += 1

    # Garde à vue (anti-doublon)
    if gav not in (None, 0):
        if not Gav.objects.filter(
            unite=unite, date_interpellation=DATE, categorie_infraction="TOTAL"
        ).exists():
            Gav.objects.create(
                unite=unite,
                date_interpellation=DATE,
                categorie_infraction="TOTAL",
                nombre_gav=gav
            )
            nb_gav += 1

print(f"{nb_interpelle} interpellations et {nb_gav} GAV importées.")
