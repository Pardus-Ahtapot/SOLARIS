# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):

    definition = models.CharField(max_length=255, verbose_name=u"Açıklama")

    def __unicode__(self):
        return unicode(self.definition)

    class Meta:
        verbose_name = u"Grup"
        verbose_name_plural = u"Gruplar"


class AssetList(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name=u"IP Adresi")
    tcp = models.CommaSeparatedIntegerField(max_length=1024, null=True, blank=True)
    udp = models.CommaSeparatedIntegerField(max_length=1024, null=True, blank=True)
    definition = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Açıklama")
    group = models.ForeignKey(Group, verbose_name="Grup", blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = u"Assetlist"
        verbose_name_plural = u"Assetlistler"


class Alarm(models.Model):
    ip_address = models.CharField(max_length=255, verbose_name=u"IP Adresi")
    tcp = models.CommaSeparatedIntegerField(max_length=1024, null=True, blank=True)
    udp = models.CommaSeparatedIntegerField(max_length=1024, null=True, blank=True)

    class Meta:
        verbose_name = u"Alarm"
        verbose_name_plural = u"Alarmlar"
