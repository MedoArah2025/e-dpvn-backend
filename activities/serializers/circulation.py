from rest_framework import serializers
from ..models.circulation import (
    EnginImmobilise,
    PieceRetire,
    VitreTeintee,
)
from activities.models.circulation import ControleRoutier

class AutoUniteSerializer(serializers.ModelSerializer):
    """Base serializer pour injecter automatiquement l'unité de l'utilisateur connecté."""

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class EnginImmobiliseSerializer(AutoUniteSerializer):
    class Meta:
        model = EnginImmobilise
        fields = "__all__"
        read_only_fields = ['unite']

class PieceRetireSerializer(AutoUniteSerializer):
    class Meta:
        model = PieceRetire
        fields = "__all__"
        read_only_fields = ['unite']

class VitreTeinteeSerializer(AutoUniteSerializer):
    class Meta:
        model = VitreTeintee
        fields = "__all__"
        read_only_fields = ['unite']
# activities/serializers/circulation.py

class ControleRoutierSerializer(AutoUniteSerializer):
    class Meta:
        model = ControleRoutier
        fields = "__all__"
        read_only_fields = ['unite']
