from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from apps.habilidade.api.serializers import HabilidadeSerializer
from apps.habilidade.api.serializers import MultiplicarXpSerializer
from apps.habilidade.models import Habilidade
from apps.habilidade.models import HabilidadeUser

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer


class HabilidadeViewSet(viewsets.ModelViewSet[Habilidade]):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer

    def get_serializer_class(self) -> type[BaseSerializer[Any]]:
        if self.action == "multiplicar_xp":
            return MultiplicarXpSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="multiplicar-xp")
    def multiplicar_xp(self, request: Request, pk: int | None = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        habilidade = Habilidade.objects.get(id=pk)
        user = request.user
        multiplicador = serializer.validated_data["multiplicador"]

        habilidade_user, created = HabilidadeUser.objects.get_or_create(
            user_id=user.pk,
            habilidade=habilidade,
        )

        if created:
            habilidade_user.xp = 1
            habilidade_user.nivel = 1
            return Response(
                data={"status": "Habilidade criada com XP inicial de 1 e nível 1"},
                status=status.HTTP_201_CREATED,
            )

        # Calcular XP e nível
        params = self._CalculoParametros(
            xp_atual=habilidade_user.xp,
            lvl_atual=habilidade_user.nivel,
            multiplicador=multiplicador,
        )

        resultado = self._calcular(params)

        habilidade_user.xp = resultado.xp
        habilidade_user.nivel = resultado.nivel

        habilidade_user.save()

        return Response(status=status.HTTP_200_OK, data={"status": "XP multiplicado"})

    @dataclass
    class _CalculoParametros:
        xp_atual: Decimal
        lvl_atual: int
        multiplicador: float

    @dataclass
    class _CalculoResultado:
        xp: Decimal
        nivel: int

    def _calcular_xp_para_upar(self, nivel: int) -> int:
        """Calcula a quantidade de XP necessária para upar para o próximo nível."""
        return (30 * nivel) - 20

    def _calcular(self, params: _CalculoParametros) -> _CalculoResultado:
        novo_xp = params.xp_atual * Decimal(params.multiplicador)
        novo_nivel = params.lvl_atual
        xp_para_upar = self._calcular_xp_para_upar(novo_nivel)

        while novo_xp >= xp_para_upar:
            novo_nivel += 1
            xp_para_upar = self._calcular_xp_para_upar(novo_nivel)

        if novo_nivel > params.lvl_atual:
            novo_xp = Decimal(1)

        return self._CalculoResultado(
            xp=novo_xp,
            nivel=novo_nivel,
        )
