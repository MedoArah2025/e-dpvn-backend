from activities.models import ControleRoutier
from units.models import Unite

UNITE = Unite.objects.get(nom="SERVICE UPR")  # ← adapte si besoin !
DATE = "2025-04-30"  # ← adapte la date du contrôle

DATA = [
    # (motif, nbre_motos, nbre_autos, nbre_tricycles, observation)
    ("Défaut de casque", 679, 0, 0, ""),
    ("Motos en défaut de plaque", 307, 0, 0, ""),
    ("Véhicules en défaut de plaque", 0, 4, 0, ""),
    ("Véhicules avec vitres teintées", 0, 42, 0, ""),
    ("Véhicules immobilisés pour autres infractions", 0, 679, 0, ""),

    # ----- Tableau 2 : pièces retirées (remarque : généralement modèle différent, ici pour archivage/contrôle global) -----
    ("Défaut de casque (pièces retirées)", 509, 0, 0, ""),
    ("Défaut de plaque (pièces retirées)", 221, 0, 0, ""),
    ("Ceinture (pièces retirées)", 312, 0, 0, ""),
    ("Téléphone (pièces retirées)", 111, 0, 0, ""),
    ("Arrêt abusif (pièces retirées)", 397, 0, 0, ""),
    ("Surcharge de cabine (pièces retirées)", 8, 0, 0, ""),
    ("Feux rouges (pièces retirées)", 388, 0, 0, ""),
    ("Arrêt à double files (pièces retirées)", 194, 0, 0, ""),
    ("Sens interdit suivi (pièces retirées)", 91, 0, 0, ""),
    ("Défaut de visite technique (pièces retirées)", 341, 0, 0, ""),
    ("Défaut de la CNSS (pièces retirées)", 421, 0, 0, ""),
    ("Plaque non conforme (ancienne plaque) (pièces retirées)", 125, 0, 0, ""),
    ("Avoir abordé un carrefour sans précaution suffisante (pièces retirées)", 159, 0, 0, ""),
    ("Défaut d’assurance (pièces retirées)", 55, 0, 0, ""),
    ("Défaut de vignette (pièces retirées)", 458, 0, 0, ""),
    ("Défaut d’un phare (pièces retirées)", 22, 0, 0, ""),
    ("Défaut de feux de position (pièces retirées)", 15, 0, 0, ""),
    ("Chevauchement de la chaussée (pièces retirées)", 15, 0, 0, ""),
    ("Refus d’obtempérer (pièces retirées)", 21, 0, 0, ""),
    ("Vitres teintées (pièces retirées)", 0, 41, 0, ""),
    ("Circulation en sens inverse (pièces retirées)", 90, 0, 0, ""),
    ("Défaut de patente (pièces retirées)", 455, 0, 0, ""),
    ("Défaut de permis de taxi (pièces retirées)", 169, 0, 0, ""),
    ("Circulation à double files (pièces retirées)", 230, 0, 0, ""),
    ("Défaut de catégorie (pièces retirées)", 18, 0, 0, ""),
    ("Défaut de feux de stop (pièces retirées)", 25, 0, 0, ""),
    ("Défaut de clignotant (pièces retirées)", 45, 0, 0, ""),
    ("Défaut de rétroviseur (pièces retirées)", 41, 0, 0, ""),
    ("Surcharge des passagers (pièces retirées)", 17, 0, 0, ""),
    ("Non-respect au panneau de stop (pièces retirées)", 85, 0, 0, ""),
    ("Défaut de feux de gabarit (pièces retirées)", 5, 0, 0, ""),
    ("Usure pneumatique (pièces retirées)", 7, 0, 0, ""),
    ("Défaut de triangle de panne (pièces retirées)", 5, 0, 0, ""),
    ("Arrêt dans un virage (pièces retirées)", 275, 0, 0, ""),
    ("Refus de priorité (pièces retirées)", 123, 0, 0, ""),
    ("Engagement imprudent (pièces retirées)", 263, 0, 0, ""),
    ("Conducteur non maître de son volant (pièces retirées)", 4, 0, 0, ""),
    ("Défaut de plaque (pièces retirées)", 215, 0, 0, ""),
    ("Ouvrage non contourné par la droite (pièces retirées)", 35, 0, 0, ""),
    ("Plaque non conforme (pièces retirées)", 65, 0, 0, ""),
    ("Non-respect de l’heure de pointe (pièces retirées)", 11, 0, 0, ""),
    # Total général non importé (c’est une synthèse)
]

nb_imports = 0

for motif, nbre_motos, nbre_autos, nbre_tricycles, observation in DATA:
    if ControleRoutier.objects.filter(
        unite=UNITE, date_controle=DATE, motif=motif
    ).exists():
        print(f"Déjà existant : {motif}")
        continue
    ControleRoutier.objects.create(
        unite=UNITE,
        date_controle=DATE,
        motif=motif,
        nbre_motos=nbre_motos or 0,
        nbre_autos=nbre_autos or 0,
        nbre_tricycles=nbre_tricycles or 0,
        observation=observation,
    )
    nb_imports += 1

print(f"{nb_imports} contrôles routiers importés pour l’unité {UNITE.nom} à la date {DATE}.")
