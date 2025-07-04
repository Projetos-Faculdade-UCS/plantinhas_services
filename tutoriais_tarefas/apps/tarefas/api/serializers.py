from apps.tarefas.models import Etapa
from apps.tarefas.models import Material
from apps.tarefas.models import MaterialTarefa
from apps.tarefas.models import Tarefa
from apps.tarefas.models import TarefaHabilidade

from django.core import validators

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


# CREATE SERIALIZERS


class MaterialTarefaCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=100)
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2)
    unidade = serializers.CharField(max_length=50, default="un")


class EtapaCreateSerializer(serializers.Serializer):
    descricao = serializers.CharField()
    ordem = serializers.IntegerField()


class TutorialCreateSerializer(serializers.Serializer):
    materiais = MaterialTarefaCreateSerializer(many=True)
    etapas = EtapaCreateSerializer(many=True)


class HabilidadeCreateSerializer(serializers.Serializer):
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

    class Meta:
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

    def create(self, validated_data: dict) -> Tarefa:
        # Extrair dados aninhados
        print(validated_data)
        habilidade_data = validated_data.pop("habilidade")
        tutorial_data = validated_data.pop("tutorial")

        # 1. Criar ou buscar TarefaHabilidade
        tarefa_habilidade, created = TarefaHabilidade.objects.get_or_create(
            habilidade_id=habilidade_data["id"],
            defaults={"multiplicador_xp": habilidade_data["multiplicador_xp"]},
        )

        # 2. Criar Tarefa
        tarefa = Tarefa.objects.create(habilidade=tarefa_habilidade, **validated_data)

        # 3. Criar Materiais e MaterialTarefa
        for material_data in tutorial_data["materiais"]:
            # Criar ou buscar Material
            material, created = Material.objects.get_or_create(
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
