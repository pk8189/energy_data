from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from common.utils import check_upload_err, read_csv, dict_from_csv
from common.models import Building, Meter

def uploader(request):
    return render(request, 'uploader.html')

def upload_building(request):
    csv = request.FILES["building_csv"]
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
    csv = request.FILES["meter_csv"]
    check_upload_err(request, csv)
    keys_to_find = ["building_id", "id" ,"fuel" ,"unit"]
    csv_lines = read_csv(csv, keys_to_find)
    csv_data = dict_from_csv(csv_lines, keys_to_find)
    for entry in csv_data:
        entry["id"] = int(entry["id"])
        entry["building"] = Building.objects.get(id=int(entry["building_id"]))
        del entry["building_id"]
        new_meters = Meter(**entry)
        new_meters.save()
    return HttpResponseRedirect(reverse("upload_page"))

def upload_consumption(request):
    csv = request.FILES["consumption_csv"]
    check_upload_err(request, csv)
    keys_to_find = ["consumption", "meter_id", "reading_date_time"]
    csv_lines = read_csv(csv, keys_to_find)
    csv_data = dict_from_csv(csv_lines, keys_to_find)
    for entry in csv_data:
        entry["meter"] = Meter.objects.get(id=int(entry["meter_id"]))
        del entry["meter_id"]
        import pdb; pdb.set_trace()
        new_meters = Meter(**entry)
        new_meters.save()
    return HttpResponseRedirect(reverse("upload_page"))