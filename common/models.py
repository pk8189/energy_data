from django.db import models

class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

class Meter(models.Model):
    id = models.IntegerField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    fuel = models.CharField(max_length=128)
    unit = models.CharField(max_length=128)

class Consumption(models.Model):
    consumption = models.FloatField(default=0)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    reading_date_time = models.DateTimeField()

