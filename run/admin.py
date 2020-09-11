from django.contrib import admin

# Register your models here.

from . import models

class AthleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'checksum')
admin.site.register(models.Athlete, AthleteAdmin)
