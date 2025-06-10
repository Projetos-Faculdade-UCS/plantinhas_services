from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TarefaHabilidadeViewSet
from .views import TarefaViewSet

ROUTER = DefaultRouter()

ROUTER.register(
    prefix="habilidades",
    viewset=TarefaHabilidadeViewSet,
    basename="tarefa-habilidades",
)
ROUTER.register(
    prefix="tarefas",
    viewset=TarefaViewSet,
    basename="tarefas",
)

urlpatterns = [
    path("", include(ROUTER.urls)),
]
