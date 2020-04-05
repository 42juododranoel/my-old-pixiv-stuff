from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from kirisame.models import Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Tag, TagModelAdmin)
