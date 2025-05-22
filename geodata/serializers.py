from rest_framework import serializers
from .models import Quartier

class QuartierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quartier
        fields = ["id", "nom", "geom"]
