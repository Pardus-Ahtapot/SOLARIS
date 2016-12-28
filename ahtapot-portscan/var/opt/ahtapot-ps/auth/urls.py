from django.conf.urls import include, url

from auth.views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^authenticate/$', authenticate, name='authenticate'),
    url(r'^logout/$', logout, name='logout'),
]