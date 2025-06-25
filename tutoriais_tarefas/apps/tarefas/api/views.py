from apps.tarefas.api.serializers import TarefaHabilidadeSerializer
from apps.tarefas.api.serializers import TarefaSerializer
from apps.tarefas.models import Tarefa
from apps.tarefas.models import TarefaHabilidade

from rest_framework.viewsets import ModelViewSet


class TarefaHabilidadeViewSet(ModelViewSet[TarefaHabilidade]):
    queryset = TarefaHabilidade.objects.all()
    serializer_class = TarefaHabilidadeSerializer
    http_method_names = ["get", "post", "put", "delete"]


class TarefaViewSet(ModelViewSet[Tarefa]):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    http_method_names = ["get", "post", "put", "delete"]
