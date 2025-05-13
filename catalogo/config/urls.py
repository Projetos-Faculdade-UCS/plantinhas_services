from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.core.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
