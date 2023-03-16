from django.contrib import admin

from .forms import ClientForm
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'INN', 'status')
    # form = ClientForm

# Register your models here.
