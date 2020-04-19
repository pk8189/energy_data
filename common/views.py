from datetime import datetime
from django.db import connections
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.template.response import TemplateResponse
import django_tables2 as tables
from django.urls import reverse

from common.utils import check_upload_err, read_csv, dict_from_csv
from common.models import Building, Meter, Consumption, BuildingTable, MeterTable, ConsumptionTable

def uploader(request):
    return render(request, "uploader.html")

def visualize(request, building_id):
    args = {"building_id": building_id}
    return TemplateResponse(request, "visualizer.html", args)

def upload_building(request):
    try:
        csv = request.FILES["building_csv"]
    except:
        return HttpResponseBadRequest("No CSV in upload")
    check_upload_err(request, csv)
    keys_to_find = ["id", "name"]
    csv_lines = read_csv(csv, keys_to_find)
    csv_data = dict_from_csv(csv_lines, keys_to_find)
    for entry in csv_data:
        entry["id"] = int(entry["id"])
        new_buildings = Building(**entry)
        new_buildings.save()
    return HttpResponseRedirect(reverse("upload_page"))

def upload_meter(request):
    try:
        csv = request.FILES["meter_csv"]
    except:
        return HttpResponseBadRequest("No CSV in upload")
    check_upload_err(request, csv)
    keys_to_find = ["building_id", "id" ,"fuel" ,"unit"]
    csv_lines = read_csv(csv, keys_to_find)
    csv_data = dict_from_csv(csv_lines, keys_to_find)
    for entry in csv_data:
        entry["id"] = int(entry["id"])
        try:
            entry["building"] = Building.objects.get(id=int(entry["building_id"]))
        except:
            return HttpResponseBadRequest("Unable to find matching building for meter. Data failed to upload")
        del entry["building_id"]
        new_meters = Meter(**entry)
        new_meters.save()
    return HttpResponseRedirect(reverse("upload_page"))

def upload_consumption(request):
    try:
        csv = request.FILES["consumption_csv"]
    except:
        return HttpResponseBadRequest("No CSV in upload")
    check_upload_err(request, csv)
    keys_to_find = ["consumption", "meter_id", "reading_date_time"]
    csv_lines = read_csv(csv, keys_to_find)
    csv_data = dict_from_csv(csv_lines, keys_to_find)
    for entry in csv_data:
        try:
            entry["meter"] = Meter.objects.get(id=int(entry["meter_id"]))
        except:
            return HttpResponseBadRequest("Unable to find matching meter for consumption. Data failed to upload")
        datetime_obj = datetime.strptime(entry["reading_date_time"], "%Y-%m-%d %H:%M")
        entry["reading_date_time"] = datetime_obj
        new_consumption = Consumption(**entry)
        new_consumption.save()
    return HttpResponseRedirect(reverse("upload_page"))

def building_list(request):
    try:
        sorter = request.GET["sort"]
        table = BuildingTable(Building.objects.all().order_by(sorter))
    except:
        table = BuildingTable(Building.objects.all())
    return render(request, "explorer.html", {
        "table": table
    })

def meter_list(request, building_id):
    try:
        sorter = request.GET["sort"]
        table = MeterTable(Meter.objects.filter(building_id=building_id).order_by(sorter))
    except:
        table = MeterTable(Meter.objects.filter(building_id=building_id))
    return render(request, "explorer.html", {
        "table": table
    })

def consumption_list(request, building_id, meter_id):
    try:
        sorter = request.GET["sort"]
        table = ConsumptionTable(Consumption.objects.filter(meter_id=meter_id).order_by(sorter))
    except:
        table = ConsumptionTable(Consumption.objects.filter(meter_id=meter_id))
    return render(request, "explorer.html", {
        "table": table
    })

def kwh_data(request, building_id):
    data = Consumption.objects.filter(
        meter__building__id=building_id,
        meter__unit="kWh"
    ) \
    .extra(
        select={"day": "TO_CHAR(reading_date_time, 'YYYY-MM-DD')"}) \
            .values("day") \
            .annotate(consumption=Sum("consumption")) \
            .order_by("day")
    return JsonResponse(list(data), safe=False)

