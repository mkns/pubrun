from django.contrib import admin

# Register your models here.

from . import models

class RunnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'checksum')
admin.site.register(models.Runner, RunnerAdmin)
