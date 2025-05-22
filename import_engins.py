from activities.models import EnginImmobilise
from units.models import Unite

# Mapping pour faire correspondre les codes du tableau avec les noms en base
MAPPING = {
    "BAC": "BAC",
    "CP/AEROPORT": "AEROPORT",
    "CP/FRANCOPHONIE": "FRANCOPHONIE",
    "CP/KOUBIA": "KOUBIA",
    "CP/NIAMEY 2000": "NIAMEY 2000",
    "CP/RIVE DROITE": "RIVE DROITE",
    "CP/TALLADJE": "TALLADJE",
    "CP/YANTALA": "YANTALA",
    "CSP/STADE": "STADE",
    "CSP/WADATA": "WADATA",
    "CU": "CU",
    "PP/MARCHE BONKANEY": "MARCHE BONKANEY",
    "PP/NOUVEAU MARCHE": "NOUVEAU MARCHE",
    "PP/PETIT MARCHE": "PETIT MARCHE",
    "SERVICE CONSTAT": "SERVICE CONSTAT",
    "UPR": "UPR",
    "UPS": "UPS",
}

# Copie les lignes du tableau ici :
DATA = [
    # Unité, motos, véhicules, tricycles
    ["BAC", 96, 20, 2],
    ["CP/AEROPORT", 35, 23, 0],
    ["CP/FRANCOPHONIE", 145, 6, 1],
    ["CP/KOUBIA", 275, 1, 15],
    ["CP/NIAMEY 2000", 184, 3, 53],
    ["CP/RIVE DROITE", 79, 0, 1],
    ["CP/TALLADJE", 8, 2, 4],
    ["CP/YANTALA", 156, 4, 24],
    ["CSP/STADE", 3, 3, 0],
    ["CSP/WADATA", 15, 70, 0],
    ["CU", 243, 2, 1],
    ["PP/MARCHE BONKANEY", 176, 1, 15],
    ["PP/NOUVEAU MARCHE", 65, 0, 0],
    ["PP/PETIT MARCHE", 258, 0, 2],
    ["SERVICE CONSTAT", 29, 1, 1],
    ["UPR", 986, 985, 107],
    ["UPS", 1677, 46, 30],
]

DATE = "2025-04-30"

compteur = 0
for row in DATA:
    code, motos, vehicules, tricycles = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    EnginImmobilise.objects.create(
        unite=unite,
        date_immobilisation=DATE,
        motos=motos,
        vehicules=vehicules,
        tricycles=tricycles,
    )
    compteur += 1

print(f"{compteur} engins immobilisés importés avec succès.")
