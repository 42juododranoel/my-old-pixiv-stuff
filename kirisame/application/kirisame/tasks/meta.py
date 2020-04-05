from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def update_meta(*args, **kwargs):
    output = StringIO()
    call_command(
        'update_meta',
        artwork_ids=kwargs['artwork_ids'],
        bot_account=kwargs['bot_account'],
        published_at=kwargs['published_at'],
        stdout=output,
    )
    return output.getvalue()
