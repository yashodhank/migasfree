# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from migasfree.server.models import Property, MigasLink


class AttributeManager(models.Manager):
    def create(self, property_att, value, description=None):
        """
        if value = "text~other", description = "other"
        """
        if '~' in value:
            value, description = value.split('~')

        queryset = Attribute.objects.filter(
            property_att=property_att, value=value
        )
        if queryset.exists():
            return queryset[0]

        attribute = Attribute()
        attribute.property_att = property_att
        attribute.value = value
        attribute.description = description
        attribute.save()

        return attribute


class Attribute(models.Model, MigasLink):
    property_att = models.ForeignKey(
        Property,
        verbose_name=_("Property")
    )

    value = models.CharField(
        verbose_name=_("value"),
        max_length=250
    )

    description = models.TextField(
        verbose_name=_("description"),
        null=True,
        blank=True
    )

    _exclude_links = ["computer - tags", ]

    objects = AttributeManager()

    def property_link(self):
        return self.property_att.link()

    property_link.short_description = _("Property")
    property_link.allow_tags = True

    def __unicode__(self):
        return '%s-%s' % (
            self.property_att.prefix,
            self.value,
        )

    def total_computers(self, version=None):
        from migasfree.server.models import Login
        if version:
            return Login.objects.filter(
                attributes__id=self.id,
                computer__version_id=version.id
            ).count()
        else:
            return Login.objects.filter(attributes__id=self.id).count()
    total_computers.admin_order_field = 'total_computers'

    def update_description(self, new_value):
        if self.description != new_value:
            self.description = new_value
            self.save()

    def delete(self, *args, **kwargs):
        # Not allowed delete atributte 'SET-ALL SYSTEM' or CID Property.prefix
        if not (self.property_att.prefix in ["CID", ] or self.id == 1):
            super(Attribute, self).delete(*args, **kwargs)

    class Meta:
        app_label = 'server'
        verbose_name = _("Attribute")
        verbose_name_plural = _("Attributes")
        unique_together = (("property_att", "value"),)
        permissions = (("can_save_attribute", "Can save Attribute"),)


class Tag(Attribute):
    _include_links = ["computer - tags", ]

    class Meta:
        app_label = 'server'
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        proxy = True


class Att(Attribute):

    class Meta:
        app_label = 'server'
        verbose_name = _("Attribute/Tag")
        verbose_name_plural = _("Attributes/Tags")
        proxy = True