# geodata/models.py

from django.db import models

class Quartier(models.Model):
    nom  = models.CharField(max_length=100, unique=True)
    geom = models.JSONField(
        help_text="Géométrie GeoJSON du quartier"
    )

    def __str__(self):
        return self.nom


