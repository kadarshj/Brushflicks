# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-21 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_usersample'),
    ]

    operations = [
        migrations.AddField(
            model_name='gethired',
            name='count_interest',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gethired',
            name='count_view',
            field=models.IntegerField(default=0),
        ),
    ]
