# -*- coding: utf-8 -*-

import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from migasfree.server.models import DeviceConnection, DeviceModel


class Device(models.Model):
    name = models.CharField(
        _("name"),
        max_length=50,
        null=True,
        blank=True,
        unique=True
    )

    model = models.ForeignKey(
        DeviceModel,
        verbose_name=_("model")
    )

    connection = models.ForeignKey(
        DeviceConnection,
        verbose_name=_("connection")
    )

    data = models.TextField(
        _("data"),
        null=True,
        blank=False,
        default="{}"
    )

    def datadict(self):
        return {
            'name': self.name,
            'model': self.model.name,
            self.connection.name: json.loads(self.data),
        }

    def __unicode__(self):
        return u'%s__%s__%s' % (
            self.name,
            self.model.name,
            self.connection.name
        )

    class Meta:
        app_label = 'server'
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        unique_together = (("connection", "name"),)
        permissions = (("can_save_device", "Can save Device"),)
