from activities.models import Infraction
from units.models import Unite

MAPPING = {
    "CCN": "SPJA/CCN",
    "Boukoki": "BOUKOKI",
    "Koubia": "KOUBIA",
    "Yantala": "YANTALA",
    "Aéroport": "AEROPORT",
    "Talladjé": "TALLADJE",
    "CPVF": "FRANCOPHONIE",
    "Kirkissoye": "KIRKISSOYE",
    "Niamey 2000": "NIAMEY 2000",
    "Rive droite": "RIVE DROITE",
    "Route Kollo": "ROUTE KOLLO",
}

DATE = "2025-04-30"  # à changer selon la période visée

DATA = [
    ["Vols (tous genre)", 28, 20, 7, 10, 2, 15, 7, 1, 5, 7, 3, 105],
    # ... (toutes les autres lignes du tableau) ...
    ["Découverte de cadavre", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

UNITE_COLS = [
    "CCN",
    "Boukoki",
    "Koubia",
    "Yantala",
    "Aéroport",
    "Talladjé",
    "CPVF",
    "Kirkissoye",
    "Niamey 2000",
    "Rive droite",
    "Route Kollo"
]

nb_created = 0
nb_skipped = 0

for row in DATA:
    infraction, *values, total = row
    for idx, col in enumerate(UNITE_COLS):
        count = values[idx]
        if not count or count == 0:
            continue
        nom_unite = MAPPING.get(col)
        if not nom_unite:
            print(f"Unité inconnue: {col}")
            continue
        try:
            unite = Unite.objects.get(nom=nom_unite)
        except Unite.DoesNotExist:
            print(f"Unité non trouvée: {nom_unite}")
            continue

        # Vérifie si l'enregistrement existe déjà (anti-doublon)
        if Infraction.objects.filter(
            unite=unite,
            date_infraction=DATE,
            categorie_infraction=infraction
        ).exists():
            nb_skipped += 1
            continue

        Infraction.objects.create(
            unite=unite,
            date_infraction=DATE,
            categorie_infraction=infraction,
            victime_homme=0,
            victime_femme=0,
            victime_mineur=0,
            mise_cause=0,
            nationaux=0,
            etrangers=0,
            refugies=0,
            immigres=0,
        )
        nb_created += 1

print(f"{nb_created} infractions importées.")
print(f"{nb_skipped} lignes déjà présentes, sautées (aucun doublon créé).")
