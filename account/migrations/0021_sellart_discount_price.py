# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-31 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20171230_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellart',
            name='discount_price',
            field=models.IntegerField(default=0),
        ),
    ]
