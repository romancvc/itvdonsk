import uuid

from .models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'INN', 'status']

    def create(self, validated_data):
        client = super().create(validated_data)
        client.save()
        return client

    def update(self, instance, validated_data):
        client = super().update(instance, validated_data)
        client.save()
        return client

