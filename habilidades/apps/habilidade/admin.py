from django.contrib import admin

from .models import Habilidade, HabilidadeUser


class MyAdminSite(admin.AdminSite):
    site_header = "Habilidades Admin"


admin_site = MyAdminSite(name="myadmin")
admin_site.register(Habilidade)
admin_site.register(HabilidadeUser)
