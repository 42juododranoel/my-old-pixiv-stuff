from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Artwork, ArtworkMeta, Bot


class Command(BaseCommand):
    help = _('Update meta')

    def add_arguments(self, parser):
        parser.add_argument('-ai', '--artwork-ids')
        parser.add_argument('-ba', '--bot-account')
        parser.add_argument('-pa', '--published-at')

    def handle(self, *args, **options):
        bot = Bot.objects.get(account=options['bot_account'])

        for artwork_id in options['artwork_ids']:
            artwork = Artwork.objects.get(id=artwork_id)
            artwork_meta = ArtworkMeta.objects.create(
                artwork=artwork,
                bot=bot,
                published_at=options['published_at'],
            )

        self.stdout.write(self.style.SUCCESS(f'Done.'))
