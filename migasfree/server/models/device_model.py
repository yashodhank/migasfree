# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from . import DeviceType, DeviceManufacturer, DeviceConnection, MigasLink


@python_2_unicode_compatible
class DeviceModel(models.Model, MigasLink):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=50,
        null=True,
        blank=True
    )

    manufacturer = models.ForeignKey(
        DeviceManufacturer,
        on_delete=models.CASCADE,
        verbose_name=_("manufacturer")
    )

    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        verbose_name=_("type")
    )

    connections = models.ManyToManyField(
        DeviceConnection,
        blank=True,
        verbose_name=_("connections")
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ", "_")
        super(DeviceModel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'server'
        verbose_name = _("Model")
        verbose_name_plural = _("Models")
        unique_together = (("device_type", "manufacturer", "name"),)
        permissions = (("can_save_devicemodel", "Can save Device Model"),)
        ordering = ['manufacturer', 'name']
