from django.urls import (
    include,
    path,
)
from django.contrib import admin
from apps.habilidade.admin import admin_site

urlpatterns = [
    path("", include("apps.habilidade.urls")),
    path("admin/", admin_site.urls),
]
