# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20170426_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winning_team',
            field=models.CharField(choices=[('HOME', 'Home Team'), ('AWAY', 'Away Team')], default=None, max_length=20),
        ),
    ]