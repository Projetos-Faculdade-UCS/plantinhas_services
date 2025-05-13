from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalogo.apps.catalogo"
    verbose_name = _("Catalogo")
    label = "catalogo"
