from activities.models import DecouverteCadavre, Incendie, Noyade
from units.models import Unite

MAPPING = {
    "CP/BOUKOKI": "BOUKOKI",
    "CP/FRANCOPHONIE": "FRANCOPHONIE",
    "CP/NIAMEY 2000": "NIAMEY 2000",
    "CP/RIVE DROITE": "RIVE DROITE",
    "CP/TALLADJE": "TALLADJE",
    "CP/YANTALA": "YANTALA",
    "CSP/WADATA": "WADATA",
    "SPJA/CCN": "SPJA/CCN",
}

DATE = "2025-04-30"

DATA = [
    # [Unité, Découverte de cadavre, Incendie, Noyade]
    ["CP/BOUKOKI", 2, None, None],
    ["CP/FRANCOPHONIE", 1, 1, 1],
    ["CP/NIAMEY 2000", 1, None, None],
    ["CP/RIVE DROITE", 1, None, 1],
    ["CP/TALLADJE", 2, 1, 0],
    ["CP/YANTALA", 2, None, None],
    ["CSP/WADATA", 4, None, None],
    ["SPJA/CCN", 4, None, None],
]

nb_cadavre = 0
nb_incendie = 0
nb_noyade = 0

for row in DATA:
    code, nb_cad, nb_inc, nb_noy = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Découvertes de cadavre
    if nb_cad not in (None, 0):
        if not DecouverteCadavre.objects.filter(
            unite=unite, date_signalement=DATE
        ).exists():
            DecouverteCadavre.objects.create(
                unite=unite,
                date_signalement=DATE,
                hommes=nb_cad,
                femmes=0,
                mineurs=0,
                faits=""
            )
            nb_cadavre += 1

    # Incendies
    if nb_inc not in (None, 0):
        if not Incendie.objects.filter(
            unite=unite, date_signalement=DATE
        ).exists():
            Incendie.objects.create(
                unite=unite,
                date_signalement=DATE,
                cause_incendie="Incendie volontaire"
            )
            nb_incendie += 1

    # Noyades
    if nb_noy not in (None, 0):
        if not Noyade.objects.filter(
            unite=unite, date_noyade=DATE
        ).exists():
            Noyade.objects.create(
                unite=unite,
                date_noyade=DATE,
                hommes=nb_noy,
                femmes=0,
                mineurs=0,
                faits=""
            )
            nb_noyade += 1

print(f"{nb_cadavre} découvertes de cadavre, {nb_incendie} incendies, {nb_noyade} noyades importées.")
