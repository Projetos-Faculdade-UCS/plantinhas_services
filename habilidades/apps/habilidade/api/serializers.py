from typing import TypedDict

from apps.habilidade.models import Habilidade
from apps.habilidade.models import HabilidadeUser

from rest_framework import serializers


class HabilidadeSerializer(serializers.ModelSerializer[Habilidade]):
    class Meta:  # type: ignore
        model = Habilidade
        fields = ["id", "nome"]

    def validate_nome(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError(
                "O nome da habilidade não pode ser vazio."
            )
        return value


class HabilidadeUserSerializer(serializers.ModelSerializer[HabilidadeUser]):
    habilidade = HabilidadeSerializer()

    class Meta:  # type: ignore
        model = HabilidadeUser
        fields = [
            "user_id",
            "habilidade",
            "xp",
            "nivel",
        ]
        read_only_fields = ["user_id", "habilidade"]
        depth = 1
        extra_kwargs = {
            "xp": {"min_value": 0, "max_value": 10},
            "nivel": {"min_value": 1},
        }

    def validate_xp(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("XP não pode ser negativo.")
        if value > 10:
            raise serializers.ValidationError("XP não pode ser maior que 10.")
        return value


class MultiplicarXpModel(TypedDict):
    habilidade_id: int
    multiplicador: float


class MultiplicarXpSerializer(serializers.Serializer[MultiplicarXpModel]):
    habilidade_id = serializers.IntegerField(required=True)
    multiplicador = serializers.FloatField(required=True, min_value=1)

    class Meta:  # type: ignore
        fields = ["habilidade_id", "multiplicador"]
