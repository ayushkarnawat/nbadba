# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 21:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20170426_2103'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='coach',
            table='Coaches',
        ),
        migrations.AlterModelTable(
            name='game',
            table='Games',
        ),
        migrations.AlterModelTable(
            name='owner',
            table='Owners',
        ),
        migrations.AlterModelTable(
            name='player',
            table='Players',
        ),
        migrations.AlterModelTable(
            name='team',
            table='Teams',
        ),
    ]
