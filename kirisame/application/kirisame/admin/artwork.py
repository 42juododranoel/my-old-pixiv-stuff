from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Artwork


class ArtworkModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'artist', 'bookmarks_count', 'published_at']


admin.site.register(Artwork, ArtworkModelAdmin)
