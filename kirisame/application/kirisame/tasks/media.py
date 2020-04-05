from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def download_media(*args, **kwargs):
    output = StringIO()
    call_command(
        'download_media',
        toot_id=kwargs['toot_id'],
        stdout=output,
    )
    return output.getvalue()
