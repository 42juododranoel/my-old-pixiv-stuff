from django.db import models
from django.utils.translation import ugettext_lazy as _


class Artist(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    account = models.CharField(
        max_length=255,
        verbose_name=_('Account'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')
