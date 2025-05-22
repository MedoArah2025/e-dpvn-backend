# activities/views/test.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Si besoin

class TestAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # décommente pour sécuriser

    def get(self, request):
        return Response({"message": "Test API OK !", "user": str(request.user)})
