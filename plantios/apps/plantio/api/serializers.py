from typing import Any
from typing import TypedDict

from apps.plantio.models import Plantio

from django.utils.timezone import now

from rest_framework import serializers


class Indicador(TypedDict):
    """TypedDict for Indicador field representation."""

    label: str
    value: float


class SaudeField(serializers.Field):  # type: ignore
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
            if isinstance(data, dict) and "value" in data:
                value = float(data["value"])
            else:
                # If data is a simple value
                value = float(data)

            # Validate range
            if not 0 <= value <= 1:
                raise serializers.ValidationError(
                    "Saúde deve ser um valor entre 0 e 1."
                )
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Saúde deve ser um valor numérico entre 0 e 1."
            )


class SedeField(serializers.Field):  # type: ignore
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
                value = float(data["value"])
            else:
                # If data is a simple value
                value = float(data)

            # Validate range
            if not 0 <= value <= 1:
                raise serializers.ValidationError("Sede deve ser um valor entre 0 e 1.")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Sede deve ser um valor numérico entre 0 e 1."
            )


class PlantioSerializer(serializers.ModelSerializer[Plantio]):
    """Serializer for Plantio model."""

    saude = serializers.SerializerMethodField()
    sede = serializers.SerializerMethodField()
    data_colheita = serializers.DateField(source="data_prevista_colheita")

    # Additional fields for write operations
    saude_update = SaudeField(write_only=True, required=False)
    sede_update = SedeField(write_only=True, required=False)

    def get_saude(self, instance: Plantio) -> Indicador:
        """Get the health status of the plant."""
        # Recalculate health and water needs if the last update was before planting
        if (
            instance.data_atualizacao_saude < now()
            and self.context.get("request", {}).method == "GET"
        ):
            # if method is GET, recalculate health
            self._recalcular_saude(instance)
            instance.save(update_fields=["saude", "data_atualizacao_saude"])

        return SaudeField().to_representation(instance.saude)

    def get_sede(self, instance: Plantio) -> Indicador:
        """Get the water needs of the plant."""
        # Recalculate health and water needs if the last update was before planting
        # and if method is get
        print(self.context.get("request", {}).method)
        if (
            instance.data_atualizacao_sede < now()
            and self.context.get("request", {}).method == "GET"
        ):
            self._recalcular_sede(instance)
            instance.save(update_fields=["sede", "data_atualizacao_sede"])

        return SedeField().to_representation(instance.sede)

    class Meta:  # type: ignore
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
            "saude_update",
            "sede_update",
        ]
        read_only_fields = ["id"]

    def _recalcular_saude(self, instance: Plantio) -> None:
        """Recalculate health based on the current state."""
        data_ultima_atualizacao_saude = instance.data_atualizacao_saude
        delta_dias_saude = (now() - data_ultima_atualizacao_saude).days

        # Recalculate health
        # in 7 days, health decreases to 0, so we calculate the health based on the days since the last update
        if delta_dias_saude > 0:
            instance.saude = max(
                0, instance.saude - (delta_dias_saude / 7) * instance.saude
            )
            instance.data_atualizacao_saude = now()

    def _recalcular_sede(self, instance: Plantio) -> None:
        """Recalculate water needs based on the current state."""
        data_ultima_atualizacao_sede = instance.data_atualizacao_sede
        delta_dias_sede = (now() - data_ultima_atualizacao_sede).days

        # Recalculate water needs
        if delta_dias_sede > 0:
            instance.sede = max(
                0, instance.sede - (delta_dias_sede / 7) * instance.sede
            )
            instance.data_atualizacao_sede = now()

    def to_internal_value(self, data: Any) -> Any:
        """Convert input data to internal representation."""
        # Map saude and sede to their update fields
        if (
            self.context.get("request", {}).method == "PATCH"
            or self.context.get("request", {}).method == "PUT"
        ):
            if "saude" in data:
                data["saude_update"] = data.pop("saude")
            if "sede" in data:
                data["sede_update"] = data.pop("sede")

        return super().to_internal_value(data)

    def update(self, instance: Plantio, validated_data: Any) -> Plantio:
        print("Updating Plantio instance with data:", validated_data)

        # Handle custom fields first and remove them from validated_data
        if "sede_update" in validated_data:
            instance.data_atualizacao_sede = now()
            instance.sede = validated_data.pop("sede_update")
        if "saude_update" in validated_data:
            instance.data_atualizacao_saude = now()
            instance.saude = validated_data.pop("saude_update")

        # Let the parent class handle the remaining fields
        return super().update(instance, validated_data)
