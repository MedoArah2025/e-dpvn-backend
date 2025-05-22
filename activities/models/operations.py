from django.db import models
from .base import BaseActivity

# Modèle abstrait pour factoriser les champs communs
class OperationActivity(BaseActivity):
    date_operation = models.DateField()
    personne_interpellees = models.PositiveIntegerField(default=0)
    mendiants_interpelles = models.PositiveIntegerField(default=0)
    charettes_pouspous = models.PositiveIntegerField(default=0)
    objet_saisie = models.CharField(
        max_length=50,
        choices=[
            ("Drogue", "Drogue"),
            ("Arme Blanche", "Arme Blanche"),
            ("Autres", "Autres"),
        ],
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

# Modèles concrets (pas abstraits !)
class Positionnement(BaseActivity):
    date_operation = models.DateField()
    lieux_position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Positionnements ({self.date_operation})"

class ServiceOrdre(BaseActivity):
    date_operation = models.DateField()
    lieux_service = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Services d’ordre ({self.date_operation})"

class Patrouille(OperationActivity):
    def __str__(self):
        return f"{self.unite.nom} – Patrouille ({self.date_operation})"

class CoupPoing(OperationActivity):
    def __str__(self):
        return f"{self.unite.nom} – Coup de poing ({self.date_operation})"

class Raffle(OperationActivity):
    def __str__(self):
        return f"{self.unite.nom} – Raffle ({self.date_operation})"

class Descente(OperationActivity):
    def __str__(self):
        return f"{self.unite.nom} – Descente ({self.date_operation})"
