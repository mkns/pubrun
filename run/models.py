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
    """ foo """
    STATUS = (
        ('registered', 'Registered'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
    )
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, default=0)
    date = models.DateField(null=False)
    time = models.TimeField(null=False, default="18:00")
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default='registered',
    )
    def __str__(self):
        return str(self.athlete)
    class Meta:
        verbose_name = "Run"
        unique_together = ('athlete', 'date')
