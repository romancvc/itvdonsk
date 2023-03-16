import uuid

from .models import TgEvent
from rest_framework import serializers


class TgEventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)

    class Meta:
        model = TgEvent
        fields = ['id', 'event_number', 'client', 'date_time', 'event_topic', 'event_description']

    def create(self, validated_data):
        tg_event = super().create(validated_data)
        tg_event.save()
        return tg_event
