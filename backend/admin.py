from __future__ import unicode_literals

from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Team)
admin.site.register(models.Player)
admin.site.register(models.GameScore)
admin.site.register(models.Game)
admin.site.register(models.Coach)
admin.site.register(models.Owner)
admin.site.register(models.PlaysIn)
