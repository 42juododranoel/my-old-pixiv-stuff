from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import ArtistMeta, ArtworkMeta


class ArtistMetaModelAdmin(admin.ModelAdmin):
    list_display = ['artist', 'published_at']


class ArtworkMetaModelAdmin(admin.ModelAdmin):
    list_display = ['artwork', 'published_at']


admin.site.register(ArtistMeta, ArtistMetaModelAdmin)
admin.site.register(ArtworkMeta, ArtworkMetaModelAdmin)
