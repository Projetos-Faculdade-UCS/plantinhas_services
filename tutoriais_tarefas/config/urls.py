from django.urls import include
from django.urls import path

urlpatterns = [
    path("tarefas/", include("apps.tarefas.urls", namespace="tarefas")),
    path("tutoriais/", include("apps.tutoriais.urls", namespace="tutoriais")),
]
