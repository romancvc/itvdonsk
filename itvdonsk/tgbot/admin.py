from django.contrib import admin

from .models import TgEvent


@admin.register(TgEvent)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_number', 'client', 'event_topic')

