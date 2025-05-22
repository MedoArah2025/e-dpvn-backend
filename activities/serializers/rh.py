from rest_framework import serializers
from ..models.rh import EffectifRH

# Mixin pour remplir unite automatiquement
class AutoUniteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)
    def update(self, instance, validated_data):
        # On ne doit jamais changer l’unité après création
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class EffectifRHSerializer(AutoUniteSerializer):
    class Meta:
        model = EffectifRH
        fields = "__all__"
        read_only_fields = ['unite']
