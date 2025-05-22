from rest_framework import serializers
from ..models.dispositions import (
    MiseslctCto,
    MiseDPJ,
    MiseDispositionOcrit,
    MiseDispositionDouane,
    MiseDST,
    MiseDPMF,
    MisePavillonE,
    MiseSoniloga,
)

# Mixin pour gérer l’unité automatiquement (copie/colle partout où besoin)
class AutoUniteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)
    def update(self, instance, validated_data):
        # Empêche modification de unite lors de l’update
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class MiseslctCtoSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseslctCto
        fields = "__all__"
        read_only_fields = ['unite']

class MiseDPJSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseDPJ
        fields = "__all__"
        read_only_fields = ['unite']

class MiseDispositionOcritSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseDispositionOcrit
        fields = "__all__"
        read_only_fields = ['unite']

class MiseDispositionDouaneSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseDispositionDouane
        fields = "__all__"
        read_only_fields = ['unite']

class MiseDSTSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseDST
        fields = "__all__"
        read_only_fields = ['unite']

class MiseDPMFSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseDPMF
        fields = "__all__"
        read_only_fields = ['unite']

class MisePavillonESerializer(AutoUniteSerializer):
    class Meta:
        model = MisePavillonE
        fields = "__all__"
        read_only_fields = ['unite']

class MiseSonilogaSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseSoniloga
        fields = "__all__"
        read_only_fields = ['unite']
