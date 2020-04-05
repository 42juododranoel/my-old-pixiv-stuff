from django.db import models
from django.utils.translation import ugettext_lazy as _


class Bot(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    account = models.CharField(
        max_length=255,
        verbose_name=_('Account'),
    )

    access_token = models.CharField(
        max_length=255,
        verbose_name=_('Access token'),
    )
    base_url = models.CharField(
        max_length=255,
        verbose_name=_('Base URL'),
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
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')
