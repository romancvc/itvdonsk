import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from data_one_c.models import Client


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    client = models.ForeignKey(Client, verbose_name='Связь с клиентом',
                               on_delete=models.SET_NULL, null=True, blank=True)

