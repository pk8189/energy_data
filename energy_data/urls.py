from django.urls import path, re_path
from django.conf import settings

API_BASE_V1 = r"^api/v1/"

from common import views

urlpatterns = [
    path("", views.uploader, name="upload_page"),
    path("explorer", views.building_list, name="building_explorer_page"),
    path("explorer/building/<int:building_id>/", views.meter_list, name="meter_explorer_page"),
    path("explorer/building/<int:building_id>/meter/<int:meter_id>/", views.consumption_list, name="consumption_explorer_page"),
    path("visualize/building/<int:building_id>/", views.visualize, name="visualize"),
    path("data/building/<int:building_id>/", views.kwh_data, name="kwh_data"),
    re_path(fr'{API_BASE_V1}building/upload_csv/$', views.upload_building, name="upload_building"),
    re_path(fr'{API_BASE_V1}meter/upload_csv/$', views.upload_meter, name="upload_meter"),
    re_path(fr'{API_BASE_V1}consumption/upload_csv/$', views.upload_consumption, name="upload_consumption"),
]