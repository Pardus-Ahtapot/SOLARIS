# -*- coding: utf-8 -*-
from django.contrib import admin


# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
from portscan.forms import *
# Register your models here.

from portscan.models import *


class AssetListAdmin(admin.ModelAdmin):
    form = AssetListForm

    list_display = ["ip_address", "tcp", "udp", "timestamp", "created_by", "definition", "group"]
    list_display_links = ["ip_address"]
    list_filter = ["ip_address", "tcp", "udp", "timestamp", "definition", "group"]
    search_fields = ["ip_address", "tcp", "udp", "definition", "group"]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


class GroupAdmin(admin.ModelAdmin):
    list_display = ["definition"]

    class Meta:
        model = Group


class AlarmAdmin(admin.ModelAdmin):

    form = AlarmForm
    list_display = ["ip_address", "tcp", "udp", "url"]

    def url(self, obj):
        filter_url = "<a href='/ps/editalarm/?alarm_id={}'>Portları Düzenle</a>".format(obj.id)
        return filter_url

    url.allow_tags = True
    url.short_description = u'Portları Düzenle'

admin.site.register(AssetList, AssetListAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Alarm, AlarmAdmin)
