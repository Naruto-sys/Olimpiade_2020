from django.db import models


class Area(models.Model):
    city = models.IntegerField('city', default=0)
    area = models.IntegerField('area', default=0)
    house = models.IntegerField('house', default=0)
    flat = models.IntegerField('flat', default=0)
    indications = models.TextField('indications', max_length=1300)
