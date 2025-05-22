from rest_framework import serializers
from ..models.judiciaire import (
    PersonnesInterpelle,
    Gav,
    Deferement,
    Plainte,
    DeclarationVol,
    Infraction,
    SaisieDrogue,
    AutreSaisie,
    Requisition,
    Incendie,
    Noyade,
    DecouverteCadavre,
    PersonnesEnleve,
    VehiculeEnleve,
)

# Mixin pour injecter l’unité automatiquement (même principe que précédemment)
class AutoUniteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)
    def update(self, instance, validated_data):
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class PersonnesInterpelleSerializer(AutoUniteSerializer):
    class Meta:
        model = PersonnesInterpelle
        fields = "__all__"
        read_only_fields = ['unite']

class GavSerializer(AutoUniteSerializer):
    class Meta:
        model = Gav
        fields = "__all__"
        read_only_fields = ['unite']

class DeferementSerializer(AutoUniteSerializer):
    class Meta:
        model = Deferement
        fields = "__all__"
        read_only_fields = ['unite']

class PlainteSerializer(AutoUniteSerializer):
    class Meta:
        model = Plainte
        fields = "__all__"
        read_only_fields = ['unite']

class DeclarationVolSerializer(AutoUniteSerializer):
    class Meta:
        model = DeclarationVol
        fields = "__all__"
        read_only_fields = ['unite']

class InfractionSerializer(AutoUniteSerializer):
    class Meta:
        model = Infraction
        fields = "__all__"
        read_only_fields = ['unite']

class SaisieDrogueSerializer(AutoUniteSerializer):
    class Meta:
        model = SaisieDrogue
        fields = "__all__"
        read_only_fields = ['unite']

class AutreSaisieSerializer(AutoUniteSerializer):
    class Meta:
        model = AutreSaisie
        fields = "__all__"
        read_only_fields = ['unite']

class RequisitionSerializer(AutoUniteSerializer):
    class Meta:
        model = Requisition
        fields = "__all__"
        read_only_fields = ['unite']

class IncendieSerializer(AutoUniteSerializer):
    class Meta:
        model = Incendie
        fields = "__all__"
        read_only_fields = ['unite']

class NoyadeSerializer(AutoUniteSerializer):
    class Meta:
        model = Noyade
        fields = "__all__"
        read_only_fields = ['unite']

class DecouverteCadavreSerializer(AutoUniteSerializer):
    class Meta:
        model = DecouverteCadavre
        fields = "__all__"
        read_only_fields = ['unite']

class PersonnesEnleveSerializer(AutoUniteSerializer):
    class Meta:
        model = PersonnesEnleve
        fields = "__all__"
        read_only_fields = ['unite']

class VehiculeEnleveSerializer(AutoUniteSerializer):
    class Meta:
        model = VehiculeEnleve
        fields = "__all__"
        read_only_fields = ['unite']
