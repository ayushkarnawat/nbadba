# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 02:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20170422_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('played_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('age', models.IntegerField()),
                ('role', models.CharField(max_length=20)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Team')),
            ],
        ),
    ]