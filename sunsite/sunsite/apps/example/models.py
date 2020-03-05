from django.db import models


# Create your models here.

class Indication(models.Model):
    id = models.IntegerField('id', primary_key=True)
    values = models.TextField('Indications', max_length=1000)


class Area(models.Model):
    town = models.IntegerField('city', default=0)
    district = models.IntegerField('area', default=0)
    house = models.IntegerField('house', default=0)
    flat = models.IntegerField('flat', default=0)
    temperature = models.ForeignKey('Indication', on_delete=models.CASCADE)