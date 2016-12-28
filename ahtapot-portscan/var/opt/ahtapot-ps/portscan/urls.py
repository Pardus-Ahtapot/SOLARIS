from django.conf.urls import url

from portscan.views import *


urlpatterns = [
    url(r'^importcsv/', import_csv, name="import_csv"),
    url(r'^editalarm/', edit_alarm, name="edit_alarm"),
]
