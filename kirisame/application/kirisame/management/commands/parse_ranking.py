import os
import json

from pixivpy3 import AppPixivAPI
from django.utils.timezone import datetime
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Artwork, Artist, Tag


class Command(BaseCommand):
    help = _('Add or update artworks from Pixiv ranking')

    def add_arguments(self, parser):
        choices = [
            'day', 'week', 'month', 'day_male', 'day_female',
            'week_original', 'week_rookie', 'day_manga',
            'day_r18', 'day_male_r18', 'day_female_r18',
            'week_r18', 'week_r18g'
        ]
        parser.add_argument(
            '-m', '--mode',
            default=choices[0],
            choices=choices,
        )
        parser.add_argument('-d', '--date', help=_('Example: 2016-08-01'))
        parser.add_argument('-o', '--offset', type=int)
        parser.add_argument(
            '-c', '--count', type=int,
            help=_(
                'Will be integer-divided by 30 and run this '
                'number of times with increasing offsets'
            )
        )

    def handle(self, *args, **options):
        api = AppPixivAPI()
        response = api.login(
            os.environ.get('PIXIV_USERNAME'),
            os.environ.get('PIXIV_PASSWORD'),
        )

        if options['offset']:
            offsets = [options['offset']]
        elif options['count']:
            offsets_count = options['count'] // 30
            offsets = [i * 30 for i in range(offsets_count)]
        else:
            offsets = [None]

        for offset in offsets:
            result = api.illust_ranking(
                mode=options['mode'],
                date=options['date'],
                offset=offset,
            )
            count = len(result.illusts)
            self.stdout.write(f'Processing {count} illusts')

            for illust in result.illusts:
                self.stdout.write(f'Processing {illust.id}')

                artwork_data = {
                    'id': illust.id,
                    'title': illust.title,
                    'description': illust.caption,
                    'bookmarks_count': illust.total_bookmarks,
                    'views_count': illust.total_view,
                    'images_count': illust.page_count,
                    'source': Artwork.SOURCE_RANKING,
                }

                artwork_data['artist'] = self.process_artist(illust)

                artwork_data['published_at'] = datetime.strptime(
                    illust.create_date,
                    '%Y-%m-%dT%H:%M:%S%z'
                )

                switch_type = {
                    'illust': Artwork.TYPE_ILLUST,
                    'manga': Artwork.TYPE_MANGA,
                    'ugoira': Artwork.TYPE_UGOIRA,
                }
                artwork_data['type'] = switch_type[illust.type]

                if illust.page_count == 1:
                    image_urls = [
                        illust.meta_single_page['original_image_url']
                    ]
                else:
                    image_urls = [
                        meta['image_urls']['original']
                        for meta in illust.meta_pages
                    ]
                artwork_data['image_urls'] = json.dumps(image_urls)

                artwork, is_artwork_created = Artwork.objects.get_or_create(
                    artwork_data, id=artwork_data['id'],
                )
                is_save_needed = False
                if not is_artwork_created:
                    for key, value in artwork_data.items():
                        if getattr(artwork, key) != value:
                            setattr(artwork, key, value)
                            is_save_needed = True

                new_tags = set()
                for tag_data in illust.tags:
                    tag, is_tag_created = Tag.objects.get_or_create(**tag_data)
                    new_tags.add(tag)

                old_tags = set(artwork.tags.all())
                if new_tags != old_tags:
                    deleted_tags = old_tags - new_tags
                    for tag in deleted_tags:
                        artwork.tags.remove(tag)
                    added_tags = new_tags - old_tags
                    for tag in added_tags:
                        artwork.tags.add(tag)
                    is_save_needed = True

                if is_save_needed:
                    artwork.save()

        self.stdout.write(self.style.SUCCESS('Done.'))

    @staticmethod
    def process_artist(illust):
        artist_data = {
            'id': illust.user.id,
            'name': illust.user.name,
            'account': illust.user.account,
        }
        artist, is_artist_created = Artist.objects.get_or_create(
            artist_data,
            id=artist_data['id'],
        )
        is_save_needed = False
        if not is_artist_created:
            for key, value in artist_data.items():
                if getattr(artist, key) != value:
                    setattr(artist, key, value)
                    is_save_needed = True

        if is_save_needed:
            artist.save()

        return artist
