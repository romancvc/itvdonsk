# Generated by Django 4.1.7 on 2023-03-13 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 13, 14, 37, 5, 974012), verbose_name='Дата создания'),
        ),
    ]