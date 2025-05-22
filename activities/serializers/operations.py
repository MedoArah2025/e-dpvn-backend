from rest_framework import serializers
from ..models.operations import (
    Positionnement,
    ServiceOrdre,
    Patrouille,
    CoupPoing,
    Raffle,
    Descente,
)

# Mixin pour l’injection automatique de l’unité
class AutoUniteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)
    def update(self, instance, validated_data):
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class PositionnementSerializer(AutoUniteSerializer):
    class Meta:
        model = Positionnement
        fields = "__all__"
        read_only_fields = ['unite']

class ServiceOrdreSerializer(AutoUniteSerializer):
    class Meta:
        model = ServiceOrdre
        fields = "__all__"
        read_only_fields = ['unite']

class PatrouilleSerializer(AutoUniteSerializer):
    class Meta:
        model = Patrouille
        fields = "__all__"
        read_only_fields = ['unite']

class CoupPoingSerializer(AutoUniteSerializer):
    class Meta:
        model = CoupPoing
        fields = "__all__"
        read_only_fields = ['unite']

class RaffleSerializer(AutoUniteSerializer):
    class Meta:
        model = Raffle
        fields = "__all__"
        read_only_fields = ['unite']

class DescenteSerializer(AutoUniteSerializer):
    class Meta:
        model = Descente
        fields = "__all__"
        read_only_fields = ['unite']
