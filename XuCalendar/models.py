from django.db import models


class dates(models.Model):
    ordinal = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    week_day = models.IntegerField()
    color = models.CharField(max_length=16)
    special = models.CharField(max_length=128)