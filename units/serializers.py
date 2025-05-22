from rest_framework import serializers
from .models import Unite, ActivityGroup, UniteActivityGroup

class UniteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unite
        fields = ["id", "nom", "type", "parent", "created_at"]

class ActivityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGroup
        fields = ["id", "nom", "description", "categorie", "created_at"]

class UniteActivityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteActivityGroup
        fields = ["id", "unite", "group"]
