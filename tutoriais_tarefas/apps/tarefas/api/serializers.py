from typing import Any

from apps.core.helpers import CronHelper
from apps.tarefas.models import Etapa
from apps.tarefas.models import Material
from apps.tarefas.models import MaterialTarefa
from apps.tarefas.models import Tarefa
from apps.tarefas.models import TarefaHabilidade

from django.core import validators

from rest_framework import serializers


class EtapaSerializer(serializers.ModelSerializer[Etapa]):
    class Meta:  # type: ignore
        model = Etapa
        fields = [
            "descricao",
            "ordem",
        ]


class MaterialTarefaSerializer(serializers.ModelSerializer[MaterialTarefa]):
    nome = serializers.CharField(source="material.nome", read_only=True)

    class Meta:  # type: ignore
        model = MaterialTarefa
        fields = [
            "nome",
            "quantidade",
            "unidade",
        ]


class TutorialSerializer(serializers.Serializer[Any]):
    materiais = MaterialTarefaSerializer(many=True, read_only=True)
    etapas = EtapaSerializer(many=True, read_only=True)


class TarefaListSerializer(serializers.ModelSerializer[Tarefa]):
    concluido = serializers.BooleanField(source="concluida", read_only=True)
    quantidade_completada = serializers.IntegerField(
        source="quantidade_realizada", read_only=True
    )
    ultima_alteracao = serializers.DateTimeField(source="atualizado_em", read_only=True)
    pode_realizar_tarefa = serializers.SerializerMethodField()
    frequencia = serializers.SerializerMethodField()

    def get_pode_realizar_tarefa(self, obj: Tarefa) -> bool:
        """
        Determines if the task can be concluded based on the cron expression.
        This is a placeholder method and should be implemented with actual logic.
        """
        if bool(obj.concluida):  # type: ignore
            return False

        return CronHelper.pode_realizar_tarefa(
            obj.cron,
            obj.data_ultima_realizacao,
        )

    class Meta:  # type: ignore
        model = Tarefa
        fields = [
            "id",
            "nome",
            "concluido",
            "tipo",
            "frequencia",
            "quantidade_total",
            "quantidade_completada",
            "ultima_alteracao",
            "pode_realizar_tarefa",
        ]

    def get_frequencia(self, obj: Tarefa) -> str | None:
        return CronHelper.get_frequencia(obj.cron)


class TarefaDetailSerializer(TarefaListSerializer):
    tutorial = serializers.SerializerMethodField()
    frequencia = serializers.SerializerMethodField()
    data_proxima_ocorrencia = serializers.SerializerMethodField()
    pode_realizar_tarefa = serializers.SerializerMethodField()

    def get_tutorial(self, obj: Tarefa) -> dict[str, Any] | None:
        return {
            "materiais": MaterialTarefaSerializer(obj.materiais, many=True).data,  # type: ignore
            "etapas": EtapaSerializer(obj.etapas, many=True).data,  # type: ignore
        }

    def get_frequencia(self, obj: Tarefa) -> str | None:
        return CronHelper.get_frequencia(obj.cron)

    def get_data_proxima_ocorrencia(self, obj: Tarefa) -> float | None:
        return CronHelper.get_data_proxima_ocorrencia(obj.cron)

    def get_pode_realizar_tarefa(self, obj: Tarefa) -> bool:
        """
        Determines if the task can be concluded based on the cron expression.
        This is a placeholder method and should be implemented with actual logic.
        """
        if bool(obj.concluida):  # type: ignore
            return False

        return CronHelper.pode_realizar_tarefa(
            obj.cron,
            obj.data_ultima_realizacao,
        )

    class Meta(TarefaListSerializer.Meta):
        fields = [
            *TarefaListSerializer.Meta.fields,
            "plantio_id",
            "frequencia",
            "pode_realizar_tarefa",
            "data_proxima_ocorrencia",
            "tutorial",
        ]


class HabilidadeSerializer(serializers.ModelSerializer[TarefaHabilidade]):
    class Meta:  # type: ignore
        model = TarefaHabilidade
        fields = [
            "id",
            "multiplicador_xp",
        ]
        read_only_fields = ["id"]  # id is auto-generated, so it should be read-only


# CREATE SERIALIZERS


class MaterialTarefaCreateSerializer(serializers.Serializer[Any]):
    nome = serializers.CharField(max_length=100)
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2)
    unidade = serializers.CharField(max_length=50, default="un")


class EtapaCreateSerializer(serializers.Serializer[Any]):
    descricao = serializers.CharField()
    ordem = serializers.IntegerField()


class TutorialCreateSerializer(serializers.Serializer[Any]):
    materiais = MaterialTarefaCreateSerializer(many=True)
    etapas = EtapaCreateSerializer(many=True)


class HabilidadeCreateSerializer(serializers.Serializer[Any]):
    id = serializers.IntegerField()
    multiplicador_xp = serializers.FloatField(
        validators=[
            validators.MinValueValidator(0.1),
            validators.MaxValueValidator(10.0),
        ]
    )


class TarefaCreateSerializer(serializers.ModelSerializer[Tarefa]):
    habilidade = HabilidadeCreateSerializer(write_only=True)
    tutorial = TutorialCreateSerializer(write_only=True)

    class Meta:  # type: ignore
        model = Tarefa
        fields = [
            "plantio_id",
            "nome",
            "tipo",
            "quantidade_total",
            "cron",
            "habilidade",
            "tutorial",
        ]

    def create(self, validated_data: dict[str, Any]) -> Tarefa:
        # Extrair dados aninhados
        print(validated_data)
        habilidade_data = validated_data.pop("habilidade")
        tutorial_data = validated_data.pop("tutorial")

        # 1. Criar ou buscar TarefaHabilidade
        tarefa_habilidade, _created = TarefaHabilidade.objects.get_or_create(
            habilidade_id=habilidade_data["id"],
            defaults={"multiplicador_xp": habilidade_data["multiplicador_xp"]},
        )

        # 2. Criar Tarefa
        tarefa = Tarefa.objects.create(habilidade=tarefa_habilidade, **validated_data)

        # 3. Criar Materiais e MaterialTarefa
        for material_data in tutorial_data["materiais"]:
            # Criar ou buscar Material
            material, _created = Material.objects.get_or_create(
                nome=material_data["nome"]
            )
            # Criar MaterialTarefa
            MaterialTarefa.objects.create(
                tarefa=tarefa,
                material=material,
                quantidade=material_data["quantidade"],
                unidade=material_data["unidade"],
            )

        # 4. Criar Etapas
        for etapa_data in tutorial_data["etapas"]:
            Etapa.objects.create(
                tarefa=tarefa,
                descricao=etapa_data["descricao"],
                ordem=etapa_data["ordem"],
            )

        return tarefa
