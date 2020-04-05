from django.db import models
from django.utils.translation import ugettext_lazy as _

from kirisame.models.bot import Bot
from kirisame.models.artwork import Artwork


class ArtworkMeta(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        verbose_name=_('Artwork'),
    )
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        verbose_name=_('Bot'),
    )

    published_at = models.DateTimeField(
        verbose_name=_('Published at'),
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
        return self.artwork.title

    class Meta:
        verbose_name = _('Artwork Meta')
        verbose_name_plural = _('Artwork Metas')
