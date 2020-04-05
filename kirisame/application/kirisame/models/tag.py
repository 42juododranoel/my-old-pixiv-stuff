from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Name'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
