# activities/models/rh.py

from django.db import models
from .base import BaseActivity

class EffectifRH(BaseActivity):
    date_rapport          = models.DateField()
    cp_hommes             = models.IntegerField(default=0)
    cp_femmes             = models.IntegerField(default=0)
    op_hommes             = models.IntegerField(default=0)
    op_femmes             = models.IntegerField(default=0)
    ip_hommes             = models.IntegerField(default=0)
    ip_femmes             = models.IntegerField(default=0)
    gpx_hommes        = models.IntegerField(default=0)
    gpx_femmes  = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Rapport RH ({self.date_rapport})"  # :contentReference[oaicite:8]{index=8}:contentReference[oaicite:9]{index=9}
