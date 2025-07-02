from apps.plantas.models import Categoria
from apps.plantas.models import Planta
from apps.plantas.models import SubCategoria

from django.contrib import admin


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "dificuldade")
    search_fields = ("nome",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(SubCategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria_pai__nome")
    search_fields = ("nome",)
    list_filter = ("categoria_pai",)


# add a new section on the side menu for the admin panel
admin.site.site_header = "Administração do Catálogo de Plantas"
admin.site.site_title = "Administração do Catálogo de Plantas"
admin.site.index_title = "Bem-vindo ao painel de administração do catálogo de plantas"
