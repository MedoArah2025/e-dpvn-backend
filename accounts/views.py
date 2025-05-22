from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API CRUD pour les utilisateurs.
    Seules les personnes avec is_staff=True (vos admins métier) peuvent
    lister/créer/modifier/supprimer des users.
    """
    queryset = User.objects.all().select_related("unite")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserProfileSerializer

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)
