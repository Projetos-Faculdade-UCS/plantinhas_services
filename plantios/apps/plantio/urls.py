from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .api.views import PlantioViewSet

app_name = "plantio"

ROUTER = DefaultRouter()

ROUTER.register(
    prefix="plantios", 
    viewser=PlantioViewSet,
    basename='plantios'
)

urlpatterns = [
    path("", include(ROUTER.urls)),
]
