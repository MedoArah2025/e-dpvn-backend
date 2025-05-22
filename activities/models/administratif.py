# activities/models/administratif.py
from django.db import models
from .base import BaseActivity

class AutresDeclarations(BaseActivity):
    type_declaration = models.CharField(
        max_length=255,
        choices=[
            ("Enfant égaré", "Enfant égaré"),
            ("Adulte égaré",   "Adulte égaré"),
            ("Véhicule",       "Véhicule"),
            ("Motos",          "Motos"),
            ("Cellulaire",     "Cellulaire"),
            ("Tricycle",       "Tricycle"),
        ],
        blank=True,
        null=True,
    )
    date_declaration = models.DateField()
    statut = models.CharField(
        max_length=20,
        choices=[("Retrouvé","Retrouvé"),("En cours","En cours")],
        default="En cours",
    )
    quartier = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – {self.type_declaration} ({self.statut})"
    # défini dans model classe.txt :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

class Procuration(BaseActivity):
    date_etablissement = models.DateField()
    nbr_etablie        = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Procurations : {self.nbr_etablie}"
    # défini dans model classe.txt :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

class DeclarationPerte(BaseActivity):
    date_etablissement = models.DateField()
    nbr_etablie        = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Déclaration de perte : {self.nbr_etablie}"
    # défini dans model classe.txt :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}

class Residence(BaseActivity):
    date_etablissement = models.DateField()
    nbr_etablie        = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Certificats de résidence : {self.nbr_etablie}"
    # défini dans model classe.txt :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}

class Cin(BaseActivity):
    date_etablissement = models.DateField()
    carte_etablie      = models.IntegerField(default=0)
    carte_reprise      = models.IntegerField(default=0)
    duplicata          = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"{self.unite.nom} – CIN : {self.carte_etablie} établies, "
            f"{self.carte_reprise} reprises, {self.duplicata} duplicatas"
        )
    # défini dans model classe.txt :contentReference[oaicite:8]{index=8}:contentReference[oaicite:9]{index=9}

class AmendeForfaitaire(BaseActivity):
    date    = models.DateField()
    montant = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Amendes forfaitaires : {self.montant} FCFA"
    # défini dans model classe.txt :contentReference[oaicite:10]{index=10}:contentReference[oaicite:11]{index=11}
