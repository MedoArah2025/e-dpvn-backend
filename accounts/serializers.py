from rest_framework import serializers
from django.contrib.auth import get_user_model
from units.models import Unite, ActivityGroup

User = get_user_model()

class UniteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unite
        fields = ['id', 'nom', 'type']

class ActivityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGroup
        fields = ['id', 'nom', 'categorie']

class UserSerializer(serializers.ModelSerializer):
    unite = UniteSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "unite",
        ]
        read_only_fields = ["id"]

class UserProfileSerializer(serializers.ModelSerializer):
    unit = UniteSerializer(source='unite', read_only=True)
    activity_groups = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'unit', 'activity_groups', 'roles']

    def get_activity_groups(self, obj):
        if obj.role == 'agent' and obj.unite:
            return ActivityGroupSerializer(
                ActivityGroup.objects.filter(affectations__unite=obj.unite).distinct(),
                many=True
            ).data
        elif obj.role in ['admin', 'direction']:
            return ActivityGroupSerializer(ActivityGroup.objects.all(), many=True).data
        return []

    def get_roles(self, obj):
        return [obj.role] if obj.role else []
