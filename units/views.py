from django.shortcuts import render
from rest_framework import viewsets
from .models import Unite, ActivityGroup, UniteActivityGroup
from .serializers import UniteSerializer, ActivityGroupSerializer, UniteActivityGroupSerializer
from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent  # <-- MODIFIE ICI
from rest_framework.permissions import IsAuthenticated

class UniteViewSet(viewsets.ModelViewSet):
    queryset = Unite.objects.all()
    serializer_class = UniteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]  # <-- MODIFIE ICI

class ActivityGroupViewSet(viewsets.ModelViewSet):
    queryset = ActivityGroup.objects.all()
    serializer_class = ActivityGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]  # <-- MODIFIE ICI

class UniteActivityGroupViewSet(viewsets.ModelViewSet):
    queryset = UniteActivityGroup.objects.all()
    serializer_class = UniteActivityGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]  # <-- MODIFIE ICI
