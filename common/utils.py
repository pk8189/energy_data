from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def check_upload_err(request, csv_file):
    if not csv_file.name.endswith(".csv"):
        messages.error(request,"File is not CSV type")
        return HttpResponseRedirect(reverse("myapp:upload_csv"))

def read_csv(request, csv_file, keys_to_find):
    try:
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
    except Exception as e:
        messages.error(request, f"Unable to read CSV with error: {e}")
        return HttpResponseRedirect(reverse("myapp:upload_csv")) 
    return dict_from_csv(request, lines, keys_to_find)

def dict_from_csv(request, lines, keys_to_find):
    try:
        header_elements = lines[0].split(",") # get the headers positions for flexibility
        keys_to_find_indices = { i : header_elements.index(i) for i in keys_to_find }
        dataset = iter(lines)
        next(dataset) # now process the actual data
        data = []
        for line in dataset:
            elements = line.split(",")
            to_add = {}
            for k in keys_to_find:
                try:
                    value = elements[keys_to_find_indices[k]]
                    if value:
                        to_add[k] = value
                except:
                    continue
            if to_add:
                data.append(to_add)
        return data
    except ValueError as e:
        messages.error(request, f"Unable to parse data from CSV with error: {e}")
        return HttpResponseRedirect(reverse("myapp:upload_csv"))








