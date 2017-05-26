# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MapSizeX', models.IntegerField()),
                ('MapSizeY', models.IntegerField()),
                ('MapArray', models.BinaryField()),
                ('UnderArray', models.BinaryField()),
                ('GameState', models.IntegerField()),
                ('Mines', models.BinaryField()),
                ('Flags', models.BinaryField()),
            ],
        ),
    ]
