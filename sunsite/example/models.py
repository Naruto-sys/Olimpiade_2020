from django.db import models

# Create your models here.


class Indications(models.Model):
    town = models.IntegerField(primary_key=True)
    district = models.IntegerField(default=0)
    house = models.IntegerField(default=0)
    flat = models.IntegerField(default=0)
    tempreture = models.IntegerField(default=0)
