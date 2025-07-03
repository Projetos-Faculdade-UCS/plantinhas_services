from apps.tarefas.models import Etapa
from apps.tarefas.models import MaterialTarefa
from apps.tarefas.models import Tarefa
from apps.tarefas.models import TarefaHabilidade

from rest_framework import serializers


class EtapaSerializer(serializers.ModelSerializer[Etapa]):
    class Meta:
        model = Etapa
        fields = [
            "descricao",
            "ordem",
        ]


class MaterialTarefaSerializer(serializers.ModelSerializer[MaterialTarefa]):
    nome = serializers.CharField(source="material.nome", read_only=True)

    class Meta:
        model = MaterialTarefa
        fields = [
            "nome",  # Assuming you have a material_id field in your model
            "quantidade",
            "unidade",
        ]


class TutorialSerializer(serializers.Serializer):
    materiais = MaterialTarefaSerializer(many=True, read_only=True)
    etapas = EtapaSerializer(many=True, read_only=True)


class TarefaHabilidadeSerializer(serializers.ModelSerializer[TarefaHabilidade]):
    class Meta:  # type: ignore
        model = TarefaHabilidade
        fields = "__all__"


class TarefaSerializer(serializers.ModelSerializer[Tarefa]):
    habilidade = TarefaHabilidadeSerializer(read_only=True)
    habilidade_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        queryset=TarefaHabilidade.objects.all(), source="habilidade", write_only=True
    )
    tutorial = serializers.SerializerMethodField()

    def get_tutorial(self, obj: Tarefa) -> dict | None:
        return {
            "materiais": MaterialTarefaSerializer(obj.materiais, many=True).data,
            "etapas": EtapaSerializer(obj.etapas, many=True).data,
        }

    class Meta:  # type: ignore
        model = Tarefa
        fields = [
            "id",
            "nome",
            "concluida",
            "tipo",
            "quantidade_total",
            "quantidade_realizada",
            "atualizado_em",
            "cron",
            "habilidade",  # For reading
            "criado_em",
            "data_conclusao",
            "habilidade_id",  # For writing
            "tutorial",  # For reading
        ]
        read_only_fields = [
            "id",
            "atualizado_em",
            "criado_em",
        ]
