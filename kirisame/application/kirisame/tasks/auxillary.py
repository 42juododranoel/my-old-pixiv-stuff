from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def remove_old_toots(*args, **kwargs):
    output = StringIO()
    call_command(
        'remove_old_toots',
        stdout=output,
    )
    return output.getvalue()
