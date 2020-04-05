from mastodon import Mastodon
from django.core.management import call_command
from django.utils.timezone import now, timedelta
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class Command(BaseCommand):
    help = _('Remove toots older than two weeks')

    def handle(self, *args, **options):
        toot_ids = Toot.objects \
            .filter(
                state=Toot.STATE_PUBLISHED,
                published_at__lte=now() - timedelta(days=14)
            ) \
            .values_list('id', flat=True)
        for toot_id in toot_ids:
            call_command(
                'remove_toot',
                toot_id=toot_id,
                stdout=output,
            )
        self.stdout.write(self.style.SUCCESS(f'Done.'))
