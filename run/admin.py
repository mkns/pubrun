""" Admin pish """

from django.contrib import admin

# Register your models here.

from . import models

class AthleteAdmin(admin.ModelAdmin):
    """ Nicer display within Admin section """
    list_display = ('id', 'name', 'email', 'checksum')
admin.site.register(models.Athlete, AthleteAdmin)

class RunsAdmin(admin.ModelAdmin):
    """ Nicer display within Admin section """
    list_display = ('id', 'athlete_id', 'date', 'status')
admin.site.register(models.Runs, RunsAdmin)
