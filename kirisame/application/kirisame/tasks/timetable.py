from io import StringIO

from celery import shared_task
from django.core.management import call_command


@shared_task
def generate_timetable(*args, **kwargs):
    output = StringIO()
    call_command(
        'generate_timetable',
        count=kwargs['count'],
        period=kwargs['period'],
        mode=kwargs['mode'],
        bot=kwargs['bot'],
        stdout=output,
    )
    return output.getvalue()
