from django.urls import include
from django.urls import path

app_name = "tarefas"

urlpatterns = [
    path("api/", include("apps.tarefas.api.urls")),
]
