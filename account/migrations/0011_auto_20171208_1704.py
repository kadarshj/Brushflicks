# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-08 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20171208_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='gethired',
            name='cover_logo',
            field=models.FileField(default=None, upload_to=''),
        ),
        migrations.AddField(
            model_name='hire',
            name='cover_logo',
            field=models.FileField(default=None, upload_to=''),
        ),
    ]
