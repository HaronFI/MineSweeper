# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solo', '0002_auto_20170526_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='MapList',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
