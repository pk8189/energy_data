from django.urls import path, re_path

API_BASE_V1 = r"^api/v1/"

from common.views import uploader, upload_building, upload_meter, upload_consumption

urlpatterns = [
    path("", uploader, name="upload_page"),
    re_path(fr'{API_BASE_V1}building/upload_csv/$', upload_building, name="upload_building"),
    re_path(fr'{API_BASE_V1}meter/upload_csv/$', upload_meter, name="upload_meter"),
    re_path(fr'{API_BASE_V1}consumption/upload_csv/$', upload_consumption, name="upload_consumption"),
]