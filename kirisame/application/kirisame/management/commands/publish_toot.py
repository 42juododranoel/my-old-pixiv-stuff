import os
import json

from mastodon import Mastodon
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class Command(BaseCommand):
    help = _('Publish specified toot')

    def add_arguments(self, parser):
        parser.add_argument('-t', '--toot-id')

    def handle(self, *args, **options):
        toot = Toot.objects.get(id=options['toot_id'])
        toot.publish()
        toot.save()
        self.stdout.write(self.style.SUCCESS(f'Done.'))
