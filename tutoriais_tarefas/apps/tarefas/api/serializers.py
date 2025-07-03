from apps.tarefas.models import Etapa
from apps.tarefas.models import MaterialTarefa
from apps.tarefas.models import Tarefa

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
            "nome",
            "quantidade",
            "unidade",
        ]


class TutorialSerializer(serializers.Serializer):
    materiais = MaterialTarefaSerializer(many=True, read_only=True)
    etapas = EtapaSerializer(many=True, read_only=True)


class TarefaListSerializer(serializers.ModelSerializer[Tarefa]):
    concluido = serializers.BooleanField(source="concluida", read_only=True)
    quantidade_completada = serializers.IntegerField(
        source="quantidade_realizada", read_only=True
    )
    ultima_alteracao = serializers.DateTimeField(source="atualizado_em", read_only=True)
    # TODO `pode_concluir_tarefa` é necessário calcular com o CRON

    class Meta:
        model = Tarefa
        fields = [
            "id",
            "nome",
            "concluido",
            "tipo",
            "quantidade_total",
            "quantidade_completada",
            "ultima_alteracao",
        ]


class TarefaDetailSerializer(TarefaListSerializer):
    # TODO `data_proxima_ocorrencia` deve ser calculada com o CRON
    # TODO `pode_concluir_tarefa` deve ser calculada com o CRON
    # TODO `frequencia` deve ser calculada com o CRON
    # TODO `habilidade` deve ser feita relação com o db de habilidades
    tutorial = serializers.SerializerMethodField()

    def get_tutorial(self, obj: Tarefa) -> dict | None:
        return {
            "materiais": MaterialTarefaSerializer(obj.materiais, many=True).data,
            "etapas": EtapaSerializer(obj.etapas, many=True).data,
        }

    class Meta(TarefaListSerializer.Meta):
        fields = TarefaListSerializer.Meta.fields + ["tutorial"]
