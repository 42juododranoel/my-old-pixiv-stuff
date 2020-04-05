from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Toot


class TootModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'scheduled_at', 'task_id']
    list_filter = ['state']

admin.site.register(Toot, TootModelAdmin)
