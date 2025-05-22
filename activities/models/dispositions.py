# activities/models/dispositions.py
from django.db import models
from .base import BaseActivity

class MiseslctCto(BaseActivity):
    hommes = models.IntegerField(default=0)
    femmes = models.IntegerField(default=0)
    mineurs= models.IntegerField(default=0)

    date_mise = models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – SLCT/CTO {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:48]{index=48}:contentReference[oaicite:49]{index=49}

class MiseDPJ(BaseActivity):
    hommes = models.IntegerField(default=0)
    femmes = models.IntegerField(default=0)
    mineurs= models.IntegerField(default=0)

    date_mise = models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – DPJ {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:50]{index=50}:contentReference[oaicite:51]{index=51}

class MiseDispositionOcrit(BaseActivity):
    hommes       = models.IntegerField(default=0)
    femmes       = models.IntegerField(default=0)
    mineurs      = models.IntegerField(default=0)
    date_mise    = models.DateField()
    cannabis     = models.IntegerField(default=0)
    amphetamines = models.IntegerField(default=0)
    tramadol     = models.IntegerField(default=0)
    diazepam     = models.IntegerField(default=0)
    exol         = models.IntegerField(default=0)
    crack        = models.IntegerField(default=0)
    cocaine      = models.IntegerField(default=0)
    heroine      = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.unite.nom} – OCRITIS {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:52]{index=52}:contentReference[oaicite:53]{index=53}

class MiseDispositionDouane(BaseActivity):
    quantite_marchandise = models.CharField(max_length=255)
    essence              = models.IntegerField(default=0)
    gazoil               = models.IntegerField(default=0)
    date_mise            = models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – Douane {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:54]{index=54}:contentReference[oaicite:55]{index=55}

class MiseDST(BaseActivity):
    hommes   = models.IntegerField(default=0)
    femmes   = models.IntegerField(default=0)
    mineurs  = models.IntegerField(default=0)
    date_mise= models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – DST {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:56]{index=56}:contentReference[oaicite:57]{index=57}

class MiseDPMF(BaseActivity):
    hommes   = models.IntegerField(default=0)
    femmes   = models.IntegerField(default=0)
    mineurs  = models.IntegerField(default=0)
    date_mise= models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – DPMF {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:58]{index=58}:contentReference[oaicite:59]{index=59}

class MisePavillonE(BaseActivity):
    hommes   = models.IntegerField(default=0)
    femmes   = models.IntegerField(default=0)
    mineurs  = models.IntegerField(default=0)
    date_mise= models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – Pavillon E {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:60]{index=60}:contentReference[oaicite:61]{index=61}

class MiseSoniloga(BaseActivity):
    motos       = models.IntegerField(default=0)
    vehicules   = models.IntegerField(default=0)
    date_mise   = models.DateField()

    def __str__(self):
        return f"{self.unite.nom} – Soniloga {self.date_mise}"
    # défini dans model classe.txt :contentReference[oaicite:62]{index=62}:contentReference[oaicite:63]{index=63}
