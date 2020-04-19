from django.db import models
import django_tables2 as tables

class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    def get_absolute_url(self):
        return f"explorer/building/{self.id}/"

class Meter(models.Model):
    id = models.IntegerField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    fuel = models.CharField(max_length=128)
    unit = models.CharField(max_length=128)

    def get_absolute_url(self):
        return f"meter/{self.id}/"

class Consumption(models.Model):
    consumption = models.FloatField(default=0)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    reading_date_time = models.DateTimeField()


class BuildingTable(tables.Table):
    id = tables.Column(linkify=True)
    class Meta:
        model = Building

class MeterTable(tables.Table):
    id = tables.Column(linkify=True)
    class Meta:
        model = Meter
        exclude = ["building"]

class ConsumptionTable(tables.Table):
    class Meta:
        model = Consumption
        exclude = ["meter"]