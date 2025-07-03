from apps.tutoriais.models import Etapa
from apps.tutoriais.models import MaterialTutorial
from apps.tutoriais.models import Tutorial

from rest_framework import serializers


class MaterialTutorialSerializer(serializers.ModelSerializer[MaterialTutorial]):
    nome = serializers.CharField(source="material.nome", read_only=True)

    class Meta:  # type: ignore
        model = MaterialTutorial
        fields = [
            "nome",
            "quantidade",
            "unidade",
        ]


class EtapaSerializer(serializers.ModelSerializer[Etapa]):
    class Meta:  # type: ignore
        model = Etapa
        fields = [
            "descricao",
            "ordem",
        ]


class TutorialDetailSerializer(serializers.ModelSerializer[Tutorial]):
    materiais = MaterialTutorialSerializer(many=True, read_only=True)
    etapas = EtapaSerializer(many=True, read_only=True)

    class Meta:  # type: ignore
        model = Tutorial
        fields = [
            "materiais",
            "etapas",
        ]
