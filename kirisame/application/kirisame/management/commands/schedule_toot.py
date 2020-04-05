from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class Command(BaseCommand):
    help = _('')

    def add_arguments(self, parser):
        parser.add_argument('-ti', '--toot-id')

    def handle(self, *args, **options):
        toot = Toot.objects.get(id=options['toot_id'])
        toot.schedule()
        toot.save()
        self.stdout.write(f'Done.')
