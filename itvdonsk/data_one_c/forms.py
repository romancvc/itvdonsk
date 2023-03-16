from django import forms

from data_one_c.models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            'full_name',
            'INN',
            'status',

        )
        widgets = {
            'full_name': forms.TextInput,
        }