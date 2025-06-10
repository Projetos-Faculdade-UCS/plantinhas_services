from tutoriais.models import Etapa
from tutoriais.models import Material
from tutoriais.models import MaterialTutorial
from tutoriais.models import Tutorial

from rest_framework import serializers


class MaterialSerializer(serializers.ModelSerializer[Material]):
    class Meta:  # type: ignore
        model = Material
        fields = "__all__"


class MaterialTutorialSerializer(serializers.ModelSerializer[MaterialTutorial]):
    class Meta:  # type: ignore
        model = MaterialTutorial
        fields = "__all__"


class EtapaSerializer(serializers.ModelSerializer[Etapa]):
    class Meta:  # type: ignore
        model = Etapa
        fields = "__all__"


class TutorialSerializer(serializers.ModelSerializer[Tutorial]):
    materiais = MaterialTutorialSerializer(many=True, read_only=True)
    etapas = EtapaSerializer(many=True, read_only=True)

    class Meta:  # type: ignore
        model = Tutorial
        fields = [
            "id",
            "titulo",
            "descricao",
            "criado_em",
            "atualizado_em",
            "materiais",
            "etapas",
        ]  # Explicitly listing fields to avoid potential issues with __all__ and related fields
