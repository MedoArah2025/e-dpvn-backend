# activities/serializers/spja.py

from rest_framework import serializers
from activities.models.spja import MiseADispositionSpja
from activities.serializers.circulation import AutoUniteSerializer

class MiseADispositionSpjaSerializer(AutoUniteSerializer):
    class Meta:
        model = MiseADispositionSpja
        fields = "__all__"
        read_only_fields = ["unite"]
