from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ClientSerializer
from .models import Client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]
