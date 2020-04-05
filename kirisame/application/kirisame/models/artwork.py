from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from kirisame.models.tag import Tag
from kirisame.models.artist import Artist


class Artwork(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
    )

    TYPE_ILLUST = 0
    TYPE_MANGA = 1
    TYPE_UGOIRA = 2
    TYPE_CHOICES = (
        (TYPE_ILLUST, _('Illust')),
        (TYPE_MANGA, _('Manga')),
        (TYPE_UGOIRA, _('Ugoira')),
    )
    type = models.SmallIntegerField(
        verbose_name=_('Type'),
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES[0][0],
    )

    SOURCE_RANKING = 0
    SOURCE_ARTIST = 1
    SOURCE_CHOICES = (
        (SOURCE_RANKING, _('Ranking')),
        (SOURCE_ARTIST, _('Artist')),
    )
    source = models.SmallIntegerField(
        verbose_name=_('Source'),
        choices=TYPE_CHOICES,
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name=_('Artist'),
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
    )

    views_count = models.IntegerField(
        verbose_name=_('Views count'),
    )
    bookmarks_count = models.IntegerField(
        verbose_name=_('Bookmarks count'),
    )

    images_count = models.IntegerField(
        verbose_name=_('Images count'),
    )
    image_urls = JSONField(
        verbose_name=_('Image URLs'),
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

    class Meta:
        verbose_name = _('Artwork')
        verbose_name_plural = _('Artworks')
