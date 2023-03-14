import uuid
from django.db import models
from datetime import datetime

from data_one_c.models import Client


class TgEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    event_number = models.CharField(verbose_name='Номер заявки', max_length=15,
                                    unique=True, default='БР-000')
    client = models.ForeignKey(Client, verbose_name='Клиент',
                               on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField(verbose_name='Дата создания', default=datetime.now())
    event_topic = models.CharField(verbose_name='Тема события', max_length=250,
                             default='Событие '+str(event_number)+' из телеграма')
    event_description = models.TextField(verbose_name='Описание события', null=True,
                                         blank=True)
