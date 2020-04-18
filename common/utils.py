from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def check_upload_err(request, csv_file):
    if not csv_file.name.endswith(".csv"):
        messages.error(request,"File is not CSV type")
        return HttpResponseRedirect(reverse("upload_page"))

def read_csv(csv_file, keys_to_find):
    file_data = csv_file.read().decode("utf-8").replace("\r", "").replace("\ufeff", "")
    lines = file_data.split("\n")
    return lines

def dict_from_csv(lines, keys_to_find):
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









