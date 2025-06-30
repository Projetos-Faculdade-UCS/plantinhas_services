from typing import TypedDict

from apps.plantio.models import Plantio

from rest_framework import serializers


class Indicador(TypedDict):
    """TypedDict for Indicador field representation."""

    label: str
    value: float


class SaudeField(serializers.Field):
    """Custom field for handling health status of the plant."""

    def to_representation(self, value: float) -> Indicador:
        label = ""
        if value >= 0.8:
            label = "Ótima"
        elif value >= 0.6:
            label = "Boa"
        elif value >= 0.4:
            label = "Regular"
        else:
            label = "Ruim"
        return {"label": label, "value": value}

    def to_internal_value(self, data: Indicador | float) -> float:
        try:
            # If data is a dictionary (like from a PATCH with the output format)
            print(type(data), data)
            if isinstance(data, dict) and "value" in data:
                return float(data["value"])
            # If data is a simple value
            return float(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Saúde deve ser um valor numérico entre 0 e 1."
            )


class SedeField(serializers.Field):
    """Custom field for handling the water needs of the plant."""

    def to_representation(self, value: float) -> Indicador:
        label = ""
        if value >= 0.8:
            label = "Alta"
        elif value >= 0.6:
            label = "Média"
        elif value >= 0.4:
            label = "Baixa"
        else:
            label = "Muito Baixa"
        return {"label": label, "value": value}

    def to_internal_value(self, data: Indicador | float) -> float:
        try:
            # If data is a dictionary (like from a PATCH with the output format)
            if isinstance(data, dict) and "value" in data:
                return float(data["value"])
            # If data is a sim12ple value
            return float(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Sede deve ser um valor numérico entre 0 e 1."
            )


class PlantioSerializer(serializers.ModelSerializer):
    """Serializer for Plantio model."""

    saude = SaudeField()
    sede = SedeField()
    data_colheita = serializers.DateField(source="data_prevista_colheita")

    class Meta:
        model = Plantio
        fields = [
            "id",
            "planta_id",
            "situacao",
            "saude",
            "sede",
            "data_plantio",
            "data_colheita",
            "informacoes_adicionais",
        ]
