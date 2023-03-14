# Generated by Django 4.1.7 on 2023-03-13 11:57

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_one_c', '0001_initial'),
        ('tgbot', '0002_alter_event_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='TgEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event_number', models.CharField(default=None, max_length=15, unique=True, verbose_name='Номер заявки')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2023, 3, 13, 14, 57, 1, 924274), verbose_name='Дата создания')),
                ('event_topic', models.CharField(default='Событие <django.db.models.fields.CharField> из телеграма', max_length=250, verbose_name='Тема события')),
                ('event_description', models.TextField(blank=True, null=True, verbose_name='Описание события')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_one_c.client', verbose_name='Клиент')),
            ],
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]