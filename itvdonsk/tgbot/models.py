import uuid
from django.db import models
from datetime import datetime

from data_one_c.models import Client


def event_numb_generator():
    events = TgEvent.objects.all()
    base_numb = 1
    for num in events:
        numb = num.event_number
        int_numb = numb.split('-')
        if int(int_numb[1]) > base_numb:
            base_numb = int(int_numb[1])
    base_numb = base_numb + 1
    next_numb = 'БР-000' + str(base_numb)
    return next_numb


class TgEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    event_number = models.CharField(verbose_name='Номер заявки', max_length=15,
                                    unique=True, default=event_numb_generator)
    client = models.ForeignKey(Client, verbose_name='Клиент',
                               on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField(verbose_name='Дата создания', default=datetime.now())
    event_topic = models.CharField(verbose_name='Тема события', max_length=250,
                             default=f'Заявка из телеграма')
    event_description = models.TextField(verbose_name='Описание события', null=True,
                                         blank=True)

    def __str__(self):
        return f'{self.event_topic} {self.event_number}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class TgUser(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID пользователя в Telegram', unique=True, primary_key=True)
    nickname = models.CharField(verbose_name='Имя пользователя', max_length=32)
    company = models.ForeignKey(Client, on_delete=models.SET_NULL,
                                verbose_name='Компания', blank=True,
                                null=True)

    def __str__(self):
        return f'#{self.external_id} {self.nickname} {self.company}'

    class Meta:
        verbose_name = 'Пользователь телеграм'
        verbose_name_plural = 'Пользователи телеграм'
