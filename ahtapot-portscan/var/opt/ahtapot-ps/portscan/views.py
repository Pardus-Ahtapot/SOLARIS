# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from portscan.forms import *
import csv
import codecs
import sys
from dmr_utils.logger import get_logger

@login_required
def import_csv(request):
    logger = get_logger()
    if request.method == "POST" and request.FILES:
        csvfile = request.FILES['csv_file']
        dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
        csvfile.open()
        reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter='|', dialect=dialect)
        i = 0 # skip the definition fields
        for row in reader:
            if i != 0:
                try:
                    AssetList.objects.get(ip_address=row[0])
                except ObjectDoesNotExist:
                    a_list = AssetList()
                    a_list.ip_address = row[0]
                    a_list.tcp = row[1]
                    a_list.udp = row[2]
                    a_list.definition = row[3]
                    if row[4] == '':
                        pass
                    else:
                        try:
                            group = Group.objects.get(definition=row[4])
                        except ObjectDoesNotExist:
                            group = Group()
                            group.definition = row[4]
                            group.save()
                        except Exception as e:
                            error_message = "ERROR while getting whitelist details ::: {0} ::: line {1}"\
                                                .format(str(e), sys.exc_info()[2].tb_lineno)
                            logger.send_log("error", error_message)
                            return render(request, "import_csv.html", {"message": error_message})
                        a_list.group = group
                    a_list.created_by = request.user
                    a_list.save()
                except Exception as e:
                    error_message = "ERROR while getting whitelist details ::: {0} ::: line {1}"\
                                            .format(str(e), sys.exc_info()[2].tb_lineno)
                    logger.send_log("error", error_message)
                    return render(request, "import_csv.html", {"message": error_message})
            else:
                i = 1
        context = {"message": "Başarıyla Yüklendi"}
        return render(request, "import_csv.html", context)
    else:
        return render(request, "import_csv.html")


@login_required
def edit_alarm(request):
    if request.GET:
        alarm_id = request.GET.get('alarm_id')
        alarm = Alarm.objects.get(pk=alarm_id)
        tcp_list = alarm.tcp.split(",")
        udp_list = alarm.udp.split(",")
        context = {"tcp": tcp_list, "udp": udp_list, "alarm_id":alarm_id}
        return render(request, "edit_alarm.html", context)
    elif request.POST:
        post_values = request.POST
        for key, value in post_values.iteritems():
            if key != "csrfmiddlewaretoken":
                key_fields = key.split("_")
                alarm_id = key_fields[1]
                port_type = key_fields[2]
                port = key_fields[3]

                alarm = Alarm.objects.get(pk=alarm_id)
                a_list = AssetList.objects.get(ip_address=alarm.ip_address)

                if port_type == "tcp":
                    new_port_list = []
                    port_list = alarm.tcp.split(",")
                    for p in port_list:
                        if int(p) == int(port):
                            asset_ports = a_list.tcp
                            asset_ports = asset_ports + "," + unicode(port)
                            a_list.tcp = asset_ports
                            a_list.save()
                        else:
                            new_port_list.append(p)
                    alarm.tcp = ",".join(new_port_list)
                    alarm.save()
                else:
                    new_port_list = []
                    port_list = alarm.udp.split(",")
                    for p in port_list:
                        if int(p) == int(port):
                            asset_ports = a_list.udp
                            asset_ports = asset_ports + "," +unicode(port)
                            a_list.udp = asset_ports
                            a_list.save()
                        else:
                            new_port_list.append(p)
                    alarm.udp = ",".join(new_port_list)
                    alarm.save()
        context = {"message": "Veriler Başarıyla Değiştirilmiştir"}
        return render(request, "edit_alarm.html", context)

    else:
        return HttpResponse("HATALI İSTEK")