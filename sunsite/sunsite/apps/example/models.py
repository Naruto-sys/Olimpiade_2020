from django.db import models


class Area(models.Model):
    town = models.IntegerField('city', default=0)
    district = models.IntegerField('area', default=0)
    house = models.IntegerField('house', default=0)
    flat = models.IntegerField('flat', default=0)
    temperature = models.TextField('indications', max_length=1300)
