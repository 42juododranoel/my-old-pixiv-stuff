from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Artist


class ArtistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'account']


admin.site.register(Artist, ArtistModelAdmin)
