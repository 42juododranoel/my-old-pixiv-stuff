from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Bot


class BotModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'account']


admin.site.register(Bot, BotModelAdmin)
