import re
from math import floor
from random import choice, choices

from celery import chain
from django.core.management import call_command
from django.utils.timezone import now, timedelta
from django.core.management.base import BaseCommand

from kirisame.models import Bot, Toot, Artwork, ArtistMeta, ArtworkMeta
from kirisame.tasks import download_media, schedule_toot, update_meta


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', default=48, type=int)
        parser.add_argument('-p', '--period', default=24, type=int)
        parser.add_argument('-m', '--mode')
        parser.add_argument('-b', '--bot')

    def handle(self, *args, **options):
        if options['mode'] == 'artist':
            get_artworks = self.get_artist_artworks
            get_text = self.get_artist_text
        if options['mode'] == 'ranking':
            get_artworks = self.get_ranking_artworks
            get_text = self.get_ranking_text

        artworks = get_artworks(options)
        publish_dates = self.get_publish_dates(options)
        bot = Bot.objects.get(account=options['bot'])

        self.stdout.write(f'Processing {len(artworks)} artworks')
        for artwork, publish_date in zip(artworks, publish_dates):
            self.stdout.write(f'Processing {artwork}')
            toot = Toot.objects.create(
                text=get_text(artwork),
                scheduled_at=publish_date,
                bot=bot,
            )
            toot.artworks.add(artwork)
            toot.save()

            chain(
                download_media.signature(kwargs={'toot_id': toot.id}),
                schedule_toot.signature(kwargs={'toot_id': toot.id}),
            ).apply_async()

        self.stdout.write(self.style.SUCCESS('Done.'))

    def get_publish_dates(self, options):
        offsets = choices(
            range(options['period'] * 3600),
            k=options['count'],
        )
        publish_dates = [
            now() + timedelta(seconds=offset)
            for offset in offsets
        ]
        return publish_dates

    def get_ranking_artworks(self, options):
        published_artwork_ids = list(ArtworkMeta.objects \
            .filter(bot__account=options['bot']) \
            .values_list('artwork__id', flat=True))
        base_queryset = Artwork.objects \
            .filter(
                images_count__lte=4,
                type=Artwork.TYPE_ILLUST,
                source=Artwork.SOURCE_RANKING,
            ) \
            .exclude(id__in=published_artwork_ids)

        oldest_artwork_published_at = base_queryset \
            .order_by('published_at') \
            .only('published_at') \
            .first().published_at

        chosen_artworks_ids = []
        chosen_artworks_count = 0
        previous_published_after = now()
        condition = lambda: (chosen_artworks_count != options['count']) \
            and (previous_published_after >= oldest_artwork_published_at)

        while condition():
            published_before = previous_published_after
            published_after = published_before - timedelta(days=30)

            missing_artworks_count = options['count'] - chosen_artworks_count
            limit = choice(range(1, missing_artworks_count + 1))
            artworks_ids = base_queryset \
                .filter(
                    published_at__lte=published_before,
                    published_at__gt=published_after,
                ) \
                .order_by('-bookmarks_count')[:limit] \
                .values_list('id', flat=True)
            chosen_artworks_ids.extend(artworks_ids)
            chosen_artworks_count += len(artworks_ids)

            previous_published_after = published_after

        missing_artworks_count = options['count'] - chosen_artworks_count
        if missing_artworks_count:
            artworks_ids = base_queryset \
                .exclude(id__in=chosen_artworks_ids) \
                .order_by('-bookmarks_count')[:missing_artworks_count] \
                .values_list('id', flat=True)
            chosen_artworks_ids.extend(artworks_ids)
            # if len(artworks) < missing_artworks_count:
            #  logging.warning()

        return Artwork.objects.filter(id__in=chosen_artworks_ids)

    def get_artist_artworks(self, options):
        queryset = Artwork.objects \
            .filter(images_count=1, type=Artwork.TYPE_ILLUST) \
            .order_by('-bookmarks_count')
        return queryset[:options['count']]

    def get_ranking_text(self, artwork):
        return f'{artwork.title}\nhttps://pixiv.net/i/{artwork.id}'

    def get_artist_text(self, artwork):
        return f'{artwork.title}\nhttps://pixiv.net/i/{artwork.id}'
