from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .api.views import CategoriaViewSet
from .api.views import PlantaViewSet

ROUTER = DefaultRouter()

ROUTER.register(
    prefix="categorias",
    viewset=CategoriaViewSet,
    basename="categorias",
)

ROUTER.register(
    prefix="plantas",
    viewset=PlantaViewSet,
    basename="plantas",
)

app_name = "plantas"

urlpatterns = [
    path("", include(ROUTER.urls)),
]
