from django.db import models
from .base import BaseActivity

class EnginImmobilise(BaseActivity):
    date_immobilisation = models.DateField()
    motos               = models.IntegerField(default=0)
    vehicules           = models.IntegerField(default=0)
    tricycles           = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Immobilisation du {self.date_immobilisation}"

class PieceRetire(BaseActivity):
    date_retrait = models.DateField()
    motos        = models.IntegerField(default=0)
    vehicules    = models.IntegerField(default=0)
    tricycles    = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Retrait du {self.date_retrait}"

class VitreTeintee(BaseActivity):
    date_mise     = models.DateField()
    nbr_vehicules = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – Vitres teintées {self.date_mise}"

# AJOUTE BIEN ICI, au même niveau, PAS dedans une autre classe !
class ControleRoutier(BaseActivity):
    date_controle = models.DateField()
    motif = models.CharField(max_length=255)
    nbre_motos = models.IntegerField(default=0)
    nbre_autos = models.IntegerField(default=0)
    nbre_tricycles = models.IntegerField(default=0)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.unite.nom} – Contrôle {self.motif} ({self.date_controle})"
