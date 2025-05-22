# activities/models/judiciaire.py

from django.db import models
from .base import BaseActivity
from geodata.models import Quartier

# 1) Choix groupés d’infractions
INFRACTION_CHOICES = [
    ("Atteintes contre les biens", [
        ("Vols (tous genre)", "Vols (tous genre)"),
        ("Vol aggravé", "Vol aggravé"),
        ("Vol de compteur", "Vol de compteur"),
        ("Vol de moto", "Vol de moto"),
        ("Vol à l'arraché", "Vol à l'arraché"),
        ("Vol de véhicules", "Vol de véhicules"),
        ("Vol de bétail", "Vol de bétail"),
        ("Vol de cellulaires", "Vol de cellulaires"),
        ("Complicité de vol", "Complicité de vol"),
        ("Recel", "Recel"),
        ("Abus de confiance", "Abus de confiance"),
        ("Abus de confiance par salarié", "Abus de confiance par salarié"),
        ("Escroquerie", "Escroquerie"),
        ("Escroquerie par un moyen de communication", "Escroquerie par un moyen de communication"),
        ("Dommage aux animaux", "Dommage aux animaux"),
        ("Destruction et dégradation des biens", "Destruction et dégradation des biens"),
        ("Incendie volontaire", "Incendie volontaire"),
        ("Larcins et filouterie", "Larcins et filouterie"),
        ("Jeux de hasard", "Jeux de hasard"),
        ("Saisie illégale", "Saisie illégale"),
        ("Détournement des deniers publics", "Détournement des deniers publics"),
    ]),
    ("Atteintes contre les personnes et mœurs", [
        ("Assassinat", "Assassinat"),
        ("Meurtre", "Meurtre"),
        ("Homicide involontaire", "Homicide involontaire"),
        ("Infanticide", "Infanticide"),
        ("Avortement", "Avortement"),
        ("Viol", "Viol"),
        ("Tentative de viol", "Tentative de viol"),
        ("Enlèvement et séquestration", "Enlèvement et séquestration"),
        ("Agression", "Agression"),
        ("Mise en danger de la vie d'autrui", "Mise en danger de la vie d'autrui"),
        ("Rixes et bagarres", "Rixes et bagarres"),
        ("Injures publiques", "Injures publiques"),
        ("Injure et voie de fait", "Injure et voie de fait"),
        ("Injure menace et voie de fait", "Injure menace et voie de fait"),
        ("Chantage", "Chantage"),
        ("Violence conjugale", "Violence conjugale"),
        ("Diffamation", "Diffamation"),
        ("Dénonciation calomnieuse", "Dénonciation calomnieuse"),
        ("Proxénétisme", "Proxénétisme"),
        ("Harcèlement sexuel", "Harcèlement sexuel"),
        ("Outrage à un agent", "Outrage à un agent"),
    ]),
    ("Crimes et délits contre la Constitution et la paix publique", [
        ("Faux et usage de faux", "Faux et usage de faux"),
        ("Usurpation de titre", "Usurpation de titre"),
        ("Atteintes à la sûreté de l'État", "Atteintes à la sûreté de l'État"),
        ("Rébellion", "Rébellion"),
        ("Association de malfaiteurs", "Association de malfaiteurs"),
        ("Refus d'obtempérer", "Refus d'obtempérer"),
        ("Découverte de cadavre", "Découverte de cadavre"),
    ]),
]


class PersonnesInterpelle(BaseActivity):
    date_interpellation  = models.DateField()
    categorie_infraction = models.CharField(
        max_length=100,
        choices=INFRACTION_CHOICES
    )
    nombre_pers_interp   = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Interpellations ({self.date_interpellation})"


class Gav(BaseActivity):
    date_interpellation  = models.DateField()
    categorie_infraction = models.CharField(
        max_length=100,
        choices=INFRACTION_CHOICES
    )
    nombre_gav           = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Garde à vue ({self.date_interpellation})"


class Deferement(BaseActivity):
    date_interpellation  = models.DateField()
    categorie_infraction = models.CharField(
        max_length=100,
        choices=INFRACTION_CHOICES
    )
    nombre_deferement    = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Déférements ({self.date_interpellation})"


class Plainte(BaseActivity):
    date_plainte   = models.DateField()
    nombre_plainte = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – {self.nombre_plainte} plainte(s) ({self.date_plainte})"




class Infraction(BaseActivity):
    date_infraction      = models.DateField()
    categorie_infraction = models.CharField(
        max_length=100,
        choices=INFRACTION_CHOICES
    )
    # → on rattache désormais au modèle Quartier
    quartier             = models.ForeignKey(
        Quartier,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Quartier de Niamey où l’infraction a été commise"
    )
    victime_homme        = models.IntegerField(default=0)
    victime_femme        = models.IntegerField(default=0)
    victime_mineur       = models.IntegerField(default=0)
    mise_cause           = models.IntegerField(default=0)
    nationaux            = models.IntegerField(default=0)
    etrangers            = models.IntegerField(default=0)
    refugies             = models.IntegerField(default=0)
    immigres             = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – {self.categorie_infraction} ({self.date_infraction})"


class SaisieDrogue(BaseActivity):
    date_saisie = models.DateField()

    nature      = models.CharField(
        max_length=50,
        choices=[
            ("Cannabis", "Cannabis"),
            ("Amphétamines", "Amphétamines"),
            ("Tramadol", "Tramadol"),
            ("Diazépam", "Diazépam"),
            ("Exol", "Exol"),
            ("Crack", "Crack"),
            ("Cocaïne", "Cocaïne"),
            ("Héroïne", "Héroïne"),
        ],
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.unite.nom} – Drogue ({self.date_saisie})"


class AutreSaisie(BaseActivity):
    date_saisie = models.DateField()
    nature      = models.CharField(
        max_length=50,
        choices=[
            ("Produits Prohibés","Produits Prohibés"),
            ("Saisie de Fonds","Saisie de Fonds")
        ],
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.unite.nom} – {self.nature} ({self.date_saisie})"


class Requisition(BaseActivity):
    date_mise = models.DateField()
    adresse_a = models.CharField(
        max_length=50,
        choices=[
            ("Airtel","Airtel"),
            ("Zamani","Zamani"),
            ("Moov","Moov"),
            ("NigerTelecom","NigerTelecom"),
            ("Médecin","Médecin"),
        ],
        blank=True, null=True
    )
    status    = models.CharField(
        max_length=20,
        choices=[("Encours","Encours"),("Reçu","Reçu")],
        default="Encours"
    )

    def __str__(self):
        return f"{self.unite.nom} – {self.adresse_a} ({self.status})"


class Incendie(BaseActivity):
    date_signalement = models.DateField()
    cause_incendie   = models.CharField(
        max_length=50,
        choices=[
            ("Incendie volontaire","Incendie volontaire"),
            ("Incendie involontaire","Incendie involontaire")
        ],
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.unite.nom} – Incendie ({self.date_signalement})"


class Noyade(BaseActivity):
    date_noyade = models.DateField()
    hommes      = models.IntegerField(default=0)
    femmes      = models.IntegerField(default=0)
    mineurs     = models.IntegerField(default=0)
    faits       = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – Noyade ({self.date_noyade})"


class DecouverteCadavre(BaseActivity):
    date_signalement = models.DateField()
    hommes            = models.IntegerField(default=0)
    femmes            = models.IntegerField(default=0)
    mineurs           = models.IntegerField(default=0)
    faits             = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – Découverte ({self.date_signalement})"


class PersonnesEnleve(BaseActivity):
    date_mise    = models.DateField()
    nbr_enlevees = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Enlèvements ({self.nbr_enlevees})"


class VehiculeEnleve(BaseActivity):
    date_mise   = models.DateField()
    nbr_enleves = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Véhicules enlevés ({self.nbr_enleves})"


class DeclarationVol(BaseActivity):
    date_plainte = models.DateField()
    type_vol     = models.CharField(
        max_length=100,
        choices=[
            ("Vol simple", "Vol simple"),
            ("Vol aggravé", "Vol aggravé"),
            ("Vol à l'arraché", "Vol à l'arraché"),
            ("Agression suivie de vol", "Agression suivie de vol"),
        ]
    )
    nombre_vol = models.IntegerField(default=0)
    # si vous voulez aussi rattacher un quartier ici, remplacez par ForeignKey comme ci-dessus
    quartier   = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – Vol ({self.date_plainte})"
