from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .api.views import HabilidadeViewSet

app_name = "habilidade"

ROUTER = DefaultRouter()

ROUTER.register(
    prefix="habilidades", 
    viewset=HabilidadeViewSet,
    basename='habilidades'
)

urlpatterns = [
    path("", include(ROUTER.urls)),
]
