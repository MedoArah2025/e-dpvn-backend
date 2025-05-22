from activities.models import Patrouille, CoupPoing, Descente
from units.models import Unite

MAPPING = {
    "BAC": "BAC",
    "CP/AER": "AEROPORT",
    "CP/BOU": "BOUKOKI",
    "CP/FRA": "FRANCOPHONIE",
    "CP/KIRK": "KIRKISSOYE",
    "CP/KOU": "KOUBIA",
    "CP/NIAN": "NIAMEY 2000",
    "CP/RIVE": "RIVE DROITE",
    "CP/ROU": "ROUTE KOLLO",
    "CP/TAL": "TALLADJE",
    "CP/YAN": "YANTALA",
    "CSP/G": "GRAND MARCHE",
    "CSP/ST": "STADE",
    "CSP/WAD": "WADATA",
    "CU": "CU",
    "PP/MAR": "MARCHE BONKANEY",
    "PP/PET": "PETIT MARCHE",
    "UPS": "UPS",
}

DATA = [
    ["BAC", 58, 182, 29, 3, 58, 0, 0, 0, 0],
    ["CP/AER", 25, 30, 0, 1, 1, 0, 0, 0, 0],
    ["CP/BOU", 44, 122, 0, 49, 258, 0, 1, 4, 0],
    ["CP/FRA", 32, 564, 12, 30, 53, 41, 3, 8, 0],
    ["CP/KIRK", 30, 17, 0, 2, 0, 24, 0, 0, 0],
    ["CP/KOU", 30, 101, 0, 3, 3, 0, 0, 0, 0],
    ["CP/NIAN", 29, 180, 12, 25, 174, 9, 0, 0, 0],
    ["CP/RIVE", 31, 101, 31, 48, 29, 0, 1, 3, 0],
    ["CP/ROU", 54, 100, 0, 0, 0, 0, 0, 0, 0],
    ["CP/TAL", 22, 28, 0, 4, 48, 0, 1, 3, 0],
    ["CP/YAN", 30, 205, 0, 57, 6, 0, 0, 0, 0],
    ["CSP/G", 58, 0, 0, 2, 0, 0, 0, 0, 0],
    ["CSP/ST", 11, 0, 1, 0, 0, 0, 3, 0, 0],
    ["CSP/WAD", 29, 5, 0, 8, 27, 7, 0, 0, 0],
    ["CU", 51, 11, 0, 0, 0, 0, 0, 0, 0],
    ["PP/MAR", 31, 0, 0, 0, 0, 0, 0, 0, 0],
    ["PP/PET", 76, 46, 0, 4, 42, 23, 0, 0, 0],
    ["UPS", 53, 27, 0, 0, 0, 0, 0, 0, 0],
]

DATE = "2025-04-30"

for row in DATA:
    code, pat_nb, pat_pers, pat_mend, cp_nb, cp_pers, cp_mend, des_nb, des_pers, des_mend = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    if pat_nb > 0 or pat_pers > 0 or pat_mend > 0:
        Patrouille.objects.create(
            unite=unite, date_operation=DATE,
            personne_interpellees=pat_pers,
            mendiants_interpelles=pat_mend,
        )
    if cp_nb > 0 or cp_pers > 0 or cp_mend > 0:
        CoupPoing.objects.create(
            unite=unite, date_operation=DATE,
            personne_interpellees=cp_pers,
            mendiants_interpelles=cp_mend,
        )
    if des_nb > 0 or des_pers > 0 or des_mend > 0:
        Descente.objects.create(
            unite=unite, date_operation=DATE,
            personne_interpellees=des_pers,
            mendiants_interpelles=des_mend,
        )
