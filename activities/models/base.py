# activities/models/base.py
from django.db import models
from units.models import Unite

class BaseActivity(models.Model):
    """
    Hérité par toutes les activités :
    contient l’unité, le flag brouillon et les timestamps.
    """
    unite      = models.ForeignKey(Unite, on_delete=models.CASCADE)
    brouillon  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
