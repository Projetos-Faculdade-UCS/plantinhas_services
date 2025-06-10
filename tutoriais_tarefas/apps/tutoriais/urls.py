from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .api.views import EtapaViewSet
from .api.views import MaterialTutorialViewSet
from .api.views import MaterialViewSet
from .api.views import TutorialViewSet

ROUTER = DefaultRouter()

ROUTER.register(
    prefix="materiais",
    viewset=MaterialViewSet,
    basename="materiais",
)
ROUTER.register(
    prefix="tutoriais",
    viewset=TutorialViewSet,
    basename="tutoriais",
)
ROUTER.register(
    prefix="materiais-tutoriais",
    viewset=MaterialTutorialViewSet,
    basename="materiais-tutoriais",
)
ROUTER.register(
    prefix="etapas",
    viewset=EtapaViewSet,
    basename="etapas",
)

app_name = "tutoriais"

urlpatterns = [
    path("", include(ROUTER.urls)),
]
