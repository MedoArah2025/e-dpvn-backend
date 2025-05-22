from rest_framework import serializers
from ..models.administratif import (
    AutresDeclarations,
    Procuration,
    DeclarationPerte,
    Residence,
    Cin,
    AmendeForfaitaire,
)

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

class AutresDeclarationsSerializer(AutoUniteSerializer):
    class Meta:
        model = AutresDeclarations
        fields = "__all__"
        read_only_fields = ['unite']

class ProcurationSerializer(AutoUniteSerializer):
    class Meta:
        model = Procuration
        fields = "__all__"
        read_only_fields = ['unite']

class DeclarationPerteSerializer(AutoUniteSerializer):
    class Meta:
        model = DeclarationPerte
        fields = "__all__"
        read_only_fields = ['unite']

class ResidenceSerializer(AutoUniteSerializer):
    class Meta:
        model = Residence
        fields = "__all__"
        read_only_fields = ['unite']

class CinSerializer(AutoUniteSerializer):
    class Meta:
        model = Cin
        fields = "__all__"
        read_only_fields = ['unite']

class AmendeForfaitaireSerializer(AutoUniteSerializer):
    class Meta:
        model = AmendeForfaitaire
        fields = "__all__"
        read_only_fields = ['unite']
