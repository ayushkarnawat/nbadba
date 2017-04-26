# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(GameScore)
admin.site.register(Game)
admin.site.register(Coach)
admin.site.register(Owner)
admin.site.register(PlaysIn)

# Register your models here.
