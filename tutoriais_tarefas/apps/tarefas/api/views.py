from typing import Any

from apps.tarefas.api.serializers import TarefaCreateSerializer
from apps.tarefas.api.serializers import TarefaDetailSerializer
from apps.tarefas.api.serializers import TarefaListSerializer
from apps.tarefas.models import Tarefa

from django.db import transaction

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TarefaViewSet(ModelViewSet[Tarefa]):
    queryset = Tarefa.objects.all()
    http_method_names = ["get", "post", "put"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TarefaDetailSerializer
        return TarefaListSerializer

    @transaction.atomic
    def create(self, request: "Request", *args: list[Any], **kwargs: dict[str, Any]):
        data = request.data
        plantio_id = data.get("plantio_id")
        tarefas_data = data.get("tarefas", [])

        created_tarefas: list[Tarefa] = []
        errors: list[dict[str, Any]] = []

        for i, tarefa_data in enumerate(tarefas_data):
            tarefa_data["plantio_id"] = plantio_id
            serializer = TarefaCreateSerializer(data=tarefa_data)
            if serializer.is_valid():
                tarefa = serializer.save()
                created_tarefas.append(tarefa)
            else:
                errors.append({"tarefa_index": i, "errors": serializer.errors})  # type: ignore

        if errors:
            return Response(
                {
                    "message": "Algumas tarefas não puderam ser criadas",
                    "errors": errors,
                },
                status=400,
            )

        response_serializer = TarefaListSerializer(created_tarefas, many=True)
        return Response(
            {
                "message": f"{len(created_tarefas)} tarefas criadas com sucesso",
                "plantio_id": plantio_id,
                "tarefas": response_serializer.data,  # type: ignore
            },
            status=201,
        )
