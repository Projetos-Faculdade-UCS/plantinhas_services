from typing import Any
from typing import TypedDict

from apps.plantas.models import Categoria
from apps.plantas.models import Planta

from rest_framework import serializers


class Dificuldade(TypedDict):
    """TypedDict for Dificuldade field representation."""

    label: str
    value: float


class DificuldadeField(serializers.Field):  # type: ignore
    """Custom field for handling difficulty levels.

    For GET requests: returns a dict with label and value
    For POST/PUT requests: accepts a numeric value
    """

    def to_representation(self, value: float) -> Dificuldade:
        label = ""
        if value <= 1:
            label = "Muito Fácil"
        elif value <= 2:
            label = "Fácil"
        elif value <= 3:
            label = "Médio"
        elif value <= 4:
            label = "Difícil"
        else:
            label = "Muito Difícil"

        return {"label": label, "value": float(value)}

    def to_internal_value(self, data: Dificuldade | float) -> float:
        try:
            # If data is a dictionary (like from a PATCH with the output format)
            if isinstance(data, dict) and "value" in data:
                return float(data["value"])
            # If data is a simple value
            return float(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Dificuldade deve ser um valor numérico entre 1 e 5."
            )


class NestedPlantaSerializer(serializers.ModelSerializer):  # type: ignore
    """Serializer for Planta used in CategoriaSerializer to avoid circular imports."""

    dificuldade = DificuldadeField()

    class Meta:  # type: ignore
        model = Planta
        fields = [
            "id",
            "nome",
            "foto",
            "dificuldade",
        ]


class CategoriaSerializer(serializers.ModelSerializer):  # type: ignore
    quantidade_plantas = serializers.SerializerMethodField()
    plantas = serializers.SerializerMethodField()

    def get_quantidade_plantas(self, obj: Categoria) -> int:
        """Returns the number of plants in the category."""
        return obj.plantas.count()  # type: ignore

    def get_plantas(self, obj: Categoria) -> list[NestedPlantaSerializer]:
        """Returns only the first 10 plants in the category."""
        plantas = obj.plantas.all()[:10]  # type: ignore
        return NestedPlantaSerializer(plantas, many=True).data  # type: ignore

    class Meta:  # type: ignore
        model = Categoria
        fields: list[str] = [
            "id",
            "nome",
            "descricao",
            "quantidade_plantas",
            "plantas",
        ]
        read_only_fields: list[str] = ["id"]
        extra_kwargs: dict[str, dict[str, Any]] = {
            "nome": {"required": True},
            "descricao": {"required": True},
        }


class PlantaSerializer(serializers.ModelSerializer):  # type: ignore
    categoria = CategoriaSerializer()
    dificuldade = DificuldadeField()

    class Meta:  # type: ignore
        model = Planta
        fields = [
            "id",
            "nome",
            "nome_cientifico",
            "foto",
            "horas_sol",
            "solo_ideal",
            "ventilacao",
            "temperatura_minima",
            "temperatura_ideal",
            "temperatura_maxima",
            "estacao_plantio",
            "dias_maturidade",
            "dificuldade",
            "categoria",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "nome": {"required": True},
            "nome_cientifico": {"required": True},
            "horas_sol": {"required": True},
            "solo_ideal": {"required": True},
            "ventilacao": {"required": True},
            "temperatura_minima": {"required": True},
            "temperatura_ideal": {"required": True},
            "temperatura_maxima": {"required": True},
            "estacao_plantio": {"required": True},
            "dias_maturidade": {"required": True},
        }

    def create(self, validated_data: dict[str, Any]) -> Planta:
        """Isto é feito somente quando tem um campo relacionado com outro serializer."""
        categoria_data = validated_data.pop("categoria")
        nome_categoria = categoria_data.get("nome")
        # If the category exists (by nome), get it; otherwise create it
        categoria_instance, _created = Categoria.objects.get_or_create(
            nome=nome_categoria, defaults=categoria_data
        )
        planta_instance = Planta.objects.create(
            categoria=categoria_instance, **validated_data
        )
        return planta_instance

    def update(self, instance: Planta, validated_data: dict[str, Any]) -> Planta:
        """Isto é feito somente quando tem um campo relacionado com outro serializer."""
        if "categoria" in validated_data:
            categoria_data = validated_data.pop("categoria")
            nome_categoria = categoria_data.get("nome")
            # If the category exists (by nome), get it; otherwise create it
            categoria_instance, _created = Categoria.objects.get_or_create(
                nome=nome_categoria, defaults=categoria_data
            )
            instance.categoria = categoria_instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # The get_dificuldade method is no longer needed as we use DificuldadeField
