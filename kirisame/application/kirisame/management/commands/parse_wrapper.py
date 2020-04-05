from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = _('')

    def handle(self, *args, **options):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']:
            for day in range(31):
                print(day)
                day += 1
                date = f'2018-{month}-{day}'
                call_command(
                    'parse_ranking',
                    mode='day',
                    date=date
                )
