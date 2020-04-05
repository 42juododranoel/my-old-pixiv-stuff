from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KirisameConfig(AppConfig):
    name = 'kirisame'
    verbose_name = _('Kirisame')

    def ready(self):
        import kirisame.signals
