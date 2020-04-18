from django.urls import path, re_path

API_BASE_V1 = r"^api/v1/"

from common.views import uploader, upload_building

urlpatterns = [
    path('', uploader),
    re_path(fr'{API_BASE_V1}upload/building_csv/$', upload_building, name='upload_building'),
]