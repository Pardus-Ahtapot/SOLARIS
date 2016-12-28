
from django import forms
from portscan.models import *

from collections import OrderedDict
import re
import csv

class AssetListForm(forms.ModelForm):
    class Meta:
        model = AssetList
        fields = ["ip_address", "tcp", "udp", "definition", "group"]

    def clean(self):

        reg_exp = re.compile('^[0-9]{1,5}( *, *[0-9]{1,5})*$')

        if self.cleaned_data.get('tcp'):
            if not reg_exp.match(self.cleaned_data.get('tcp')):
                raise forms.ValidationError(u'TCP port list is wrong, please check the list below for typo\'s.')

            tcpport = self.cleaned_data.get('tcp').strip().split(',')
            tcp_list = []

            for port in tcpport:
                if int(port) > 65535:
                    raise forms.ValidationError(port + " in the TCP port list is not a valid port number, please fix it.")
                tcp_list.append(port.encode('utf8').strip())

            tcp_list = list(OrderedDict.fromkeys(tcp_list))
            tcp_string = ','.join(tcp_list)
            self.cleaned_data['tcp'] = tcp_string

        if self.cleaned_data.get('udp'):
            if not reg_exp.match(self.cleaned_data.get('udp')):
                raise forms.ValidationError(u'UDP port list is wrong, please check the list below for typo\'s.')

            udpport = self.cleaned_data.get('udp').strip().split(',')
            udp_list = []

            for port in udpport:
                if int(port) > 65535:
                    raise forms.ValidationError(port + " in the UDP port list is not a valid port number, please fix it.")
                udp_list.append(port.encode('utf8').strip())


            udp_list = list(OrderedDict.fromkeys(udp_list))
            udp_string = ','.join(udp_list)

            self.cleaned_data['udp'] = udp_string

        # if there is another rule for that ip
        ip_address = self.cleaned_data.get('ip_address')
        ipcheck = AssetList.objects.filter(ip_address=ip_address).exclude(pk=self.instance.pk)

        if ipcheck.count() > 0:
            raise forms.ValidationError("A rule for this ip address already exists.")


class AlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = '__all__'

    def clean(self):
        tcpport = []
        tcp_list = []
        tcp_commaremoved_list = []
        if type(self.cleaned_data.get('tcp') == 'unicode'):
            tcpport = self.cleaned_data.get('tcp').split(",")
        else:
            tcpport = self.cleaned_data.get('tcp')

        for port in tcpport:
            tcp_list.append(port.encode('utf8').strip())

        tcp_list = list(OrderedDict.fromkeys(tcp_list))

        for port in tcp_list:
            if port is not ',':
                tcp_commaremoved_list.append(port)

        tcp_string = ','.join(tcp_commaremoved_list)
        self.cleaned_data['tcp'] = tcp_string


class DataInput(forms.Form):
    file = forms.FileField()

    def save(self):
        records = csv.reader(self.cleaned_data["file"])
        for line in records:
            input_data = AssetList()
            input_data.ip_address = line[0]
            input_data.tcp = line[1]
            input_data.udp = line[2]
            input_data.save()

