from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def schedule_toot(*args, **kwargs):
    output = StringIO()
    call_command(
        'schedule_toot',
        toot_id=kwargs['toot_id'],
        stdout=output,
    )
    return output.getvalue()


@shared_task
def publish_toot(*args, **kwargs):
    output = StringIO()
    call_command(
        'publish_toot',
        toot_id=kwargs['toot_id'],
        stdout=output,
    )
    return output.getvalue()
