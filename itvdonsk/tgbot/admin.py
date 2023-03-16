from django.contrib import admin

from .models import *


@admin.register(TgEvent)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_number', 'client', 'event_topic', 'event_description')

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'nickname', 'company')



