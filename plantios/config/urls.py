from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.plantio.urls")),
]
