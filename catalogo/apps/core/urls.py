from django.urls import include
from django.urls import path

app_name = "core"

urlpatterns = [
    path("", include("apps.plantas.urls", namespace="plantas")),
]
