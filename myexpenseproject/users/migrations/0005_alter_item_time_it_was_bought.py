# Generated by Django 4.1.1 on 2022-11-07 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_standingorder_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='time_it_was_bought',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 7, 14, 0, 40, 388095)),
        ),
    ]