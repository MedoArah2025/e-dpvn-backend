# activities/models/spja.py

from django.db import models
from .base import BaseActivity

class MiseADispositionSpja(BaseActivity):
    date_mise = models.DateField()
    objet = models.CharField(max_length=255)
    nbre_personnes = models.IntegerField(default=0)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – Mise à Disposition SPJA {self.date_mise} ({self.objet})"
