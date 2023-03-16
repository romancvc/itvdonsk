import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Client(models.Model):
    COMPANY = 'COMP'
    PRIVATE_PERSON = 'PRIV'
    BUDGET_INSTITUTION = 'BUDGET'
    USER_TYPE = [
        (COMPANY, 'Компания'),
        (PRIVATE_PERSON, 'Частное лицо/ИП'),
        (BUDGET_INSTITUTION, 'Бюджетное учреждение')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=250,
                                  unique=True, null=True, blank=True)
    INN = models.CharField(verbose_name='ИНН Физ/Юр лица', max_length=12,
                              unique=True, null=True, blank=True)
    status = models.CharField(verbose_name='Тип пользователя', max_length=50,
                              choices=USER_TYPE, default=COMPANY)
    tg_password = models.CharField(verbose_name='Пароль для авторизации в телеграм',
                                   null=True, blank=True, max_length=19)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
