from apps.tarefas.models import Tarefa
from apps.tarefas.models import TarefaHabilidade
from apps.tutoriais.api.serializers import TutorialSerializer
from apps.tutoriais.models import Tutorial  # Import Tutorial

from rest_framework import serializers


class TarefaHabilidadeSerializer(serializers.ModelSerializer[TarefaHabilidade]):
    class Meta:  # type: ignore
        model = TarefaHabilidade
        fields = "__all__"


class TarefaSerializer(serializers.ModelSerializer[Tarefa]):
    habilidade = TarefaHabilidadeSerializer(read_only=True)
    tutorial = TutorialSerializer(read_only=True)
    habilidade_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        queryset=TarefaHabilidade.objects.all(), source="habilidade", write_only=True
    )
    tutorial_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        queryset=Tutorial.objects.all(),
        source="tutorial",
        write_only=True,
        allow_null=True,  # Allow null as the model field allows null
        required=False,  # Allow blank as the model field allows blank
    )

    class Meta:  # type: ignore
        model = Tarefa
        fields = [
            "id",
            "nome",
            "tipo",
            "quantidade_total",
            "quantidade_realizada",
            "atualizado_em",
            "cron",
            "habilidade",  # For reading
            "tutorial",  # For reading
            "criado_em",
            "concluida",
            "data_conclusao",
            "habilidade_id",  # For writing
            "tutorial_id",  # For writing
        ]
        read_only_fields = [
            "id",
            "atualizado_em",
            "criado_em",
        ]
