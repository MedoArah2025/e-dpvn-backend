from django.db import models
from .base import BaseActivity

class AccidentCirculation(BaseActivity):
    """
    Concerne les constats d'accident de la circulation.
    Hérite de BaseActivity pour la FK vers l'unité et les timestamps.
    """
    date                 = models.DateField()
    homicide_involontaire= models.IntegerField(default=0)
    blesses_graves       = models.IntegerField(default=0)
    blesses_legers       = models.IntegerField(default=0)
    degats_materiels     = models.IntegerField(default=0)
    victime_hommes       = models.IntegerField(default=0)
    victime_femmes       = models.IntegerField(default=0)
    victime_mineurs      = models.IntegerField(default=0)
    cause_accident       = models.TextField(blank=True, null=True)
    profil_route         = models.CharField(max_length=255, blank=True, null=True)
    vehicule_engins      = models.CharField(max_length=255, blank=True, null=True)
    types_routes         = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name        = "Accident de circulation"
        verbose_name_plural = "Accidents de circulation"

    def __str__(self):
        return f"{self.unite.nom} – Accident du {self.date}"
