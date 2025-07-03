from apps.habilidade.admin import admin_site

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.habilidade.urls")),
    path("admin/", admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.insert(
        0,
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    )
