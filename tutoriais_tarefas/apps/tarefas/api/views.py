from typing import Any

from apps.core.helpers import CronHelper
from apps.tarefas.api.serializers import HabilidadeSerializer
from apps.tarefas.api.serializers import TarefaCreateSerializer
from apps.tarefas.api.serializers import TarefaDetailSerializer
from apps.tarefas.api.serializers import TarefaListSerializer
from apps.tarefas.models import Tarefa

from django.db import transaction

from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend


class TarefaViewSet(ModelViewSet[Tarefa]):
    queryset = Tarefa.objects.all()
    http_method_names = ["get", "post", "put"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["plantio_id"]

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

    @action(detail=True, methods=["post"])
    def realizar(self, request: "Request", pk: int | None = None):
        tarefa = self.get_object()
        if bool(tarefa.concluida):  # type: ignore
            raise NotAcceptable("Tarefa já concluída")

        pode_realizar_tarefa = CronHelper.pode_realizar_tarefa(
            tarefa.cron,
            tarefa.data_ultima_realizacao,
        )

        if not pode_realizar_tarefa:
            raise NotAcceptable(
                "Tarefa já foi realizada no período definido.",
            )

        tarefa.realizar()
        tarefa.save()

        serializer = HabilidadeSerializer(tarefa.habilidade)
        return Response(
            {
                "message": "Tarefa realizada com sucesso",
                "habilidade": serializer.data,  # type: ignore
            },
            status=200,
        )
