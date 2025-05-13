from rest_framework import serializers

from catalogo.apps.plantas.models import Categoria
from catalogo.apps.plantas.models import Planta


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome", "descricao"]
        read_only_fields = ["id"]
        extra_kwargs = {"nome": {"required": True}, "descricao": {"required": True}}


class PlantaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()

    class Meta:
        model = Planta
        fields = [
            "id",
            "nome",
            "nome_cientifico",
            "foto",
            "horas_sol",
            "solo_ideal",
            "ventilacao",
            "temperatura_ideal",
            "estacao_plantio",
            "dias_maturidade",
            "categoria",
            "dificuldade",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "nome": {"required": True},
            "nome_cientifico": {"required": True},
            "horas_sol": {"required": True},
            "solo_ideal": {"required": True},
            "ventilacao": {"required": True},
            "temperatura_ideal": {"required": True},
            "estacao_plantio": {"required": True},
            "dias_maturidade": {"required": True},
            "dificuldade": {"required": True},
        }
