from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def parse_ranking(*args, **kwargs):
    output = StringIO()
    call_command(
        'parse_ranking',
        mode=kwargs['mode'],
        stdout=output,
    )
    return output.getvalue()
