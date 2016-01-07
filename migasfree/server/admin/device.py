# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.db.models import Q

from .migasfree import MigasAdmin

from ..models import (
    DeviceType, DeviceFeature, DeviceManufacturer, DeviceConnection,
    DeviceDriver, DeviceLogical, DeviceModel, Device
)
from ..forms import DeviceLogicalForm, ExtraThinTextarea


@admin.register(DeviceType)
class DeviceTypeAdmin(MigasAdmin):
    list_display= ('name',)
    list_display_links = ('name',)
    ordering = ('name',)


@admin.register(DeviceFeature)
class DeviceFeatureAdmin(MigasAdmin):
    list_display= ('name',)
    list_display_links = ('name',)
    ordering = ('name',)


@admin.register(DeviceManufacturer)
class DeviceManufacturerAdmin(MigasAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ('name',)


@admin.register(DeviceConnection)
class DeviceConnectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fields')
    list_select_related = ('devicetype',)
    ordering = ('devicetype__name', 'name')
    fields = ('devicetype', 'name', 'fields')

    def get_form(self, request, obj=None, **kwargs):
        form = super(type(self), self).get_form(request, obj, **kwargs)
        form.base_fields['devicetype'].widget.can_add_related = False

        return form


@admin.register(DeviceDriver)
class DeviceDriverAdmin(MigasAdmin):
    list_display = ('model', 'version', 'feature', 'name')
    list_display_links = ('model',)
    fields = ('model', 'version', 'feature', 'name', 'install')

    def get_form(self, request, obj=None, **kwargs):
        form = super(type(self), self).get_form(request, obj, **kwargs)
        form.base_fields['model'].widget.can_add_related = False
        form.base_fields['version'].widget.can_add_related = False
        form.base_fields['feature'].widget.can_add_related = False

        return form


@admin.register(DeviceLogical)
class DeviceLogicalAdmin(MigasAdmin):
    form = DeviceLogicalForm
    fields = ('device', 'feature', 'computers')
    list_select_related = ('device', 'feature')
    list_display = ('link', 'device_link', 'feature')
    ordering = ('device__name', 'feature__name')
    search_fields = (
        'id',
        'device__name',
        'device__model__name',
        'device__model__manufacturer__name',
        'feature__name',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(type(self), self).get_form(request, obj, **kwargs)
        form.base_fields['device'].widget.can_add_related = False
        form.base_fields['feature'].widget.can_add_related = False

        return form


class DeviceLogicalInline(admin.TabularInline):
    model = DeviceLogical
    form = DeviceLogicalForm
    fields = ('feature', 'computers')
    extra = 0


@admin.register(Device)
class DeviceAdmin(MigasAdmin):
    list_display = ('name', 'model_link', 'connection')
    list_display_links = ('name',)
    list_filter = ('model',)
    search_fields = (
        'name',
        'model__name',
        'model__manufacturer__name'
    )
    fields = ('name', 'model', 'connection', 'data')
    ordering = ('name',)

    inlines = [DeviceLogicalInline]

    class Media:
        js = ('js/device_admin.js',)

    def save_related(self, request, form, formsets, change):
        super(type(self), self).save_related(request, form, formsets, change)
        device = form.instance

        for feature in DeviceFeature.objects.filter(
            devicedriver__model__id=device.model.id
        ).distinct():
            if DeviceLogical.objects.filter(
                Q(device__id=device.id) & Q(feature=feature)
            ).count() == 0:
                logical = device.devicelogical_set.create(
                    device=device,
                    feature=feature
                )
                logical.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(type(self), self).get_form(request, obj, **kwargs)
        form.base_fields['model'].widget.can_add_related = False
        form.base_fields['connection'].widget.can_add_related = False

        return form


class DeviceDriverInline(admin.TabularInline):
    model = DeviceDriver
    formfield_overrides = {models.TextField: {'widget': ExtraThinTextarea}}
    fields = ('version', 'feature', 'name', 'install')
    ordering = ('version', 'feature')
    extra = 1


@admin.register(DeviceModel)
class DeviceModelAdmin(MigasAdmin):
    list_display = ('name', 'manufacturer', 'devicetype')
    list_display_links = ('name',)
    list_filter = ('devicetype', 'manufacturer')
    ordering = ('devicetype__name', 'manufacturer__name', 'name')
    search_fields = (
        'name',
        'manufacturer__name',
        'connections__devicetype__name'
    )
    inlines = [DeviceDriverInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(type(self), self).get_form(request, obj, **kwargs)
        form.base_fields['manufacturer'].widget.can_add_related = False
        form.base_fields['devicetype'].widget.can_add_related = False
        form.base_fields['connections'].widget.can_add_related = False

        return form