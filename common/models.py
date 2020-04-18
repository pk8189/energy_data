from django.db import models

class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
