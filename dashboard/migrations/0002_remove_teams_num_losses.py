# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 21:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='num_losses',
        ),
    ]
