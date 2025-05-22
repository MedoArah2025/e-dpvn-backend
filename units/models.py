
from django.db import models

class Unite(models.Model):
    TYPE_CHOICES = [
        ('cp',      'Commissariat de Police'),
        ('csp',     'Commissariat Special de Police'),
        ('pp',      'Poste de Police'),
        ('ui',      'Unité d’Intervention'),
        ('constat', 'Service Constat'),
        ('upr',     'Unité de Police Routiere'),
    ]

    nom        = models.CharField(max_length=255, unique=True)
    type       = models.CharField(max_length=20, choices=TYPE_CHOICES)
    parent     = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='enfants'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"


class ActivityGroup(models.Model):
    CATEGORIES = [
        ('administratif', 'Administratif'),
        ('circulation',   'Circulation'),
        ('judiciaire',    'Judiciaire'),
        ('disposition',   'Disposition'),
        ('operation',     'Operation'),
        ('constat', 'Accident de la Ciculaion'),
        ('rh', 'Ressources Humaines'),
        ('spja', 'SPJA'),
    ]

    nom         = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    categorie   = models.CharField(max_length=20, choices=CATEGORIES)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categorie', 'nom']

    def __str__(self):
        return f"{self.nom} [{self.get_categorie_display()}]"


class UniteActivityGroup(models.Model):
    """
    Pivot : affecte un ou plusieurs groupes d’activités à chaque unité.
    """
    unite = models.ForeignKey(
        Unite,
        on_delete=models.CASCADE,
        related_name='affectations'
    )
    group = models.ForeignKey(
        ActivityGroup,
        on_delete=models.CASCADE,
        related_name='affectations'
    )

    class Meta:
        unique_together = ('unite', 'group')

    def __str__(self):
        return f"{self.unite.nom} → {self.group.nom}"
