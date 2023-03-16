from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import TgEventSerializer
from .models import TgEvent


class ClientViewSet(viewsets.ModelViewSet):
    queryset = TgEvent.objects.all()
    serializer_class = TgEventSerializer
    permission_classes = [permissions.IsAdminUser]
