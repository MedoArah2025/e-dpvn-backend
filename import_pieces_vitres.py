from activities.models import PieceRetire, VitreTeintee
from units.models import Unite

MAPPING = {
    "BAC": "BAC",
    "CP/FRANCOPHONIE": "FRANCOPHONIE",
    "CP/KOUBIA": "KOUBIA",
    "CP/NIAMEY 2000": "NIAMEY 2000",
    "CP/RIVE DROITE": "RIVE DROITE",
    "CP/TALLADJE": "TALLADJE",
    "CP/YANTALA": "YANTALA",
    "CSP/ G MARCHE": "GRAND MARCHE",
    "CSP/STADE": "STADE",
    "CSP/WADATA": "WADATA",
    "CU": "CU",
    "PP/MARCHE BONKANEY": "MARCHE BONKANEY",
    "PP/NOUVEAU MARCHE": "NOUVEAU MARCHE",
    "PP/PETIT MARCHE": "PETIT MARCHE",
    "UPR": "UPR",
}

DATA = [
    # Unité, pièces retirées, vitres teintées retirées
    ["BAC", 293, 107],
    ["CP/FRANCOPHONIE", 34, 0],
    ["CP/KOUBIA", 98, 0],
    ["CP/NIAMEY 2000", 90, 0],
    ["CP/RIVE DROITE", 22, 0],
    ["CP/TALLADJE", 0, 0],
    ["CP/YANTALA", 12, 0],
    ["CSP/ G MARCHE", 170, 4],
    ["CSP/STADE", 122, 1],
    ["CSP/WADATA", 114, 0],
    ["CU", 315, 1],
    ["PP/MARCHE BONKANEY", 9, 0],
    ["PP/NOUVEAU MARCHE", 32, 0],
    ["PP/PETIT MARCHE", 98, 0],
    ["UPR", 6087, 42],
]

DATE = "2025-04-30"

compteur_piece = 0
compteur_vitre = 0

for row in DATA:
    code, nb_pieces, nb_vitres = row
    nom_unite = MAPPING.get(code)
    if not nom_unite:
        print(f"Unité inconnue: {code}")
        continue
    try:
        unite = Unite.objects.get(nom=nom_unite)
    except Unite.DoesNotExist:
        print(f"Unité non trouvée: {nom_unite}")
        continue

    # Import des pièces retirées (PieceRetire)
    if nb_pieces > 0:
        PieceRetire.objects.create(
            unite=unite,
            date_retrait=DATE,
            motos=nb_pieces,  # ou autres champs selon le type de pièces !
            vehicules=0,
            tricycles=0,
        )
        compteur_piece += 1

    # Import des vitres teintées (VitreTeintee)
    if nb_vitres > 0:
        VitreTeintee.objects.create(
            unite=unite,
            date_mise=DATE,
            nbr_vehicules=nb_vitres
        )
        compteur_vitre += 1

print(f"{compteur_piece} pièces retirées et {compteur_vitre} vitres teintées importées.")
