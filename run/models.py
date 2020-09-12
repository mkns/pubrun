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

class Runs(models.Model):
    """ One row for every person's run """
    STATUS = (
        ('registered', 'Registered'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
    )
    athlete_id = models.IntegerField(null=False)
    date = models.DateField(null=False)
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default='registered',
    )
    def __str__(self):
        return str(self.athlete_id)
    class Meta:
        verbose_name = "Run"
        unique_together = ('athlete_id', 'date')
