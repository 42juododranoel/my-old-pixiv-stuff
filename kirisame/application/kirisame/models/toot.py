import os
import re
import json
import itertools

import cv2
from django.db import models
from mastodon import Mastodon
from pixivpy3 import AppPixivAPI
from django.utils.timezone import now
from django_fsm import FSMIntegerField, transition
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from kirisame.models.bot import Bot
from kirisame.models.artwork import Artwork
from kirisame.utils.detect_faces import detect_faces
from kirisame.tasks import publish_toot, update_meta


class Toot(models.Model):
    text = models.TextField(
        verbose_name=_('Text'),
    )

    file_names = JSONField(
        blank=True,
        null=True,
        verbose_name=_('File names'),
    )

    media_ids = JSONField(
        blank=True,
        null=True,
        verbose_name=_('Media IDs'),
    )

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        verbose_name=_('Bot'),
    )

    artworks = models.ManyToManyField(
        Artwork,
        verbose_name=_('Artworks'),
    )

    STATE_PLANNED = 0
    STATE_DOWNLOADED = 1
    STATE_SCHEDULED = 2
    STATE_PUBLISHED = 3
    STATE_REMOVED = 3
    STATE_CHOICES = (
        (STATE_PLANNED, _('Planned')),
        (STATE_DOWNLOADED, _('Downloaded')),
        (STATE_SCHEDULED, _('Scheduled')),
        (STATE_PUBLISHED, _('Published')),
        (STATE_REMOVED, _('Removed')),
    )
    state = FSMIntegerField(
        choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0],
    )

    scheduled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Scheduled at'),
    )
    task_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Task ID'),
        help_text=_('Celery task ID assigned after scheduling')
    )

    published_at = models.DateTimeField(
        verbose_name=_('Published at'),
        blank=True,
        null=True,
    )
    toot_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Toot ID'),
        help_text=_('Mastodon toot ID assigned after publishing')
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
        verbose_name = _('Toot')
        verbose_name_plural = _('Toots')

    @transition(field=state, source=STATE_PLANNED, target=STATE_DOWNLOADED)
    def download(self):
        image_urls = [
            json.loads(artwork.image_urls)
            for artwork in self.artworks.all()
        ]
        image_urls = list(itertools.chain.from_iterable(image_urls))
        urls_count = len(image_urls)
        api = AppPixivAPI()

        file_names = []
        for i, image_url in enumerate(image_urls):
            name = image_url.split('/')[-1]
            api.download(image_url, '/application/media/artworks/', name)
            file_names.append('/application/media/artworks/' + name)

        self.file_names = json.dumps(file_names)

    @transition(field=state, source=STATE_DOWNLOADED, target=STATE_SCHEDULED)
    def schedule(self):
        result = publish_toot.apply_async(
            kwargs={'toot_id': self.id},
            eta=self.scheduled_at,
        )
        self.task_id = result.id

    @transition(field=state, source=STATE_SCHEDULED, target=STATE_PUBLISHED)
    def publish(self):
        api = Mastodon(
            access_token=self.bot.access_token,
            api_base_url=self.bot.base_url,
        )
        media_ids = []
        file_names = json.loads(self.file_names)
        for file_name in file_names:
            image, faces = detect_faces(file_name)
            y, x, _ = image.shape
            image_y_center = int(y / 2)
            image_x_center = int(x / 2)

            focus = None
            # Hardcoded [:1] for now
            for x, y, w, h in faces[:1]:
                face_x_center = int((x + x + w) / 2)
                face_y_center = int((y + y + h) / 2)

                face_x_center_offset = (face_x_center / image_x_center) - 1
                face_y_center_offset = ((-1 * face_y_center) / image_y_center) + 1
                focus = (face_x_center_offset, face_y_center_offset)

            result = api.media_post(file_name, focus=focus)
            media_ids.append(result['id'])
        self.media_ids = json.dumps(media_ids)

        result = api.status_post(self.text, media_ids=media_ids)
        self.toot_id = result['id']
        self.published_at = now()

        kwargs = {
            'artwork_ids': list(self.artworks.values_list('id', flat=True)),
            'bot_account': self.bot.account,
            'published_at': self.published_at,
        }
        update_meta.apply_async(kwargs=kwargs)

    @transition(field=state, source=STATE_PUBLISHED, target=STATE_REMOVED)
    def remove(self):
        api = Mastodon(
            access_token=self.bot.access_token,
            api_base_url=self.bot.base_url,
        )
        result = api.status_delete(self.toot_id)
