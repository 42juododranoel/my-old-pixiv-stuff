from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class Command(BaseCommand):
    help = _('Download toot images and fill media_ids field')

    def add_arguments(self, parser):
        parser.add_argument('-ti', '--toot-id')

    def handle(self, *args, **options):
        toot = Toot.objects.get(id=options['toot_id'])
        toot.download()
        toot.save()
        self.stdout.write(f'Done.')
