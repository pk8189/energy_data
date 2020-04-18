from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from common.utils import check_upload_err, read_csv#, id_to_int
from common.models import Building

def uploader(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    return render(request, 'uploader.html') #context)

def upload_building(request):
    building_csv = request.FILES["building_csv"]
    check_upload_err(request, building_csv)
    keys_to_find = ["id", "name"]
    csv_data = read_csv(request, building_csv, keys_to_find)
    print(csv_data)
    import pdb; pdb.set_trace()
    #db_data = id_to_int(csv_data) update

    #new_buildings = Building(**db_data)
    #new_buildings.save()
    return HttpResponseRedirect("")
    