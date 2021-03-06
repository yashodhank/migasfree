# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from . import MigasLink


class UserManager(models.Manager):
    def create(self, name, fullname=''):
        obj = User()
        obj.name = name
        obj.fullname = fullname
        obj.save()

        return obj


@python_2_unicode_compatible
class User(models.Model, MigasLink):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=50,
        null=False
    )

    fullname = models.CharField(
        verbose_name=_("fullname"),
        max_length=100,
        blank=True
    )

    objects = UserManager()

    def __str__(self):
        if self.fullname != '':
            return u'{} ({})'.format(self.name, self.fullname.strip())

        return self.name

    class Meta:
        app_label = 'server'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        unique_together = (('name', 'fullname'),)
        permissions = (("can_save_user", "Can save User"),)
