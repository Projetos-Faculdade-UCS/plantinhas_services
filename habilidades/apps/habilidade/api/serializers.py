from decimal import Decimal
from typing import TypedDict

from apps.habilidade.models import Habilidade
from apps.habilidade.models import HabilidadeUser

from rest_framework import serializers


class HabilidadeUserSerializer(serializers.ModelSerializer[HabilidadeUser]):
    class Meta:  # type: ignore
        model = HabilidadeUser
        fields = [
            "xp",
            "nivel",
            "xp_para_upar",
            "porcentagem",
        ]
        read_only_fields = [
            "xp",
            "nivel",
            "xp_para_upar",
        ]
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


class HabilidadeSerializer(serializers.ModelSerializer[Habilidade]):
    detalhes = HabilidadeUserSerializer(
        source="habilidadeuser",
        read_only=True,
    )

    class Meta:  # type: ignore
        model = Habilidade
        fields = ["id", "nome", "descricao", "detalhes"]
        read_only_fields = ["id", "detalhes", "nome", "descricao"]


class MultiplicarXpModel(TypedDict):
    habilidade_id: int
    multiplicador: float


class MultiplicarXpSerializer(serializers.Serializer[MultiplicarXpModel]):
    multiplicador = serializers.FloatField(required=True, min_value=1)

    class Meta:  # type: ignore
        fields = ["multiplicador"]


class MultiplicarXpResponseModel(TypedDict):
    status: str
    xp_ganho: Decimal
    novo_nivel: int
