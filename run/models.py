""" All the database fun """

from django.db import models

# Create your models here.

class Athlete(models.Model):
    """ Stores details of each Runner """
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=255, null=True)
    checksum = models.CharField(max_length=8, null=True, blank=True)
    qrcodexml = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.name
