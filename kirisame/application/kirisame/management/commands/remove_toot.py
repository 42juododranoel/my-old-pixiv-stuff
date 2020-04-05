import os
import json

from mastodon import Mastodon
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class Command(BaseCommand):
    help = _('Remove specified toot')

    def add_arguments(self, parser):
        parser.add_argument('-t', '--toot-id')

    def handle(self, *args, **options):
        self.stdout.write(f'Removing toot #{options["toot_id"]}')
        toot = Toot.objects.get(id=options['toot_id'])
        toot.remove()
        toot.save()
        self.stdout.write(self.style.SUCCESS(f'Done.'))
