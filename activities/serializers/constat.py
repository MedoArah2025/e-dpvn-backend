from rest_framework import serializers
from ..models.constat import AccidentCirculation

class AutoUniteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'unite') and request.user.unite:
            validated_data['unite'] = request.user.unite
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('unite', None)
        return super().update(instance, validated_data)

class AccidentCirculationSerializer(AutoUniteSerializer):
    class Meta:
        model = AccidentCirculation
        fields = "__all__"
        read_only_fields = ['unite']
