# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-11 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_artliked'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistshare',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
