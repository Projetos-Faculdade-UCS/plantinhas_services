from dataclasses import dataclass
from typing import Any
from typing import cast

from apps.habilidade.api.serializers import HabilidadeUserSerializer
from apps.habilidade.api.serializers import MultiplicarXpSerializer
from apps.habilidade.models import Habilidade
from apps.habilidade.models import HabilidadeUser

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer


class HabilidadeViewSet(viewsets.ModelViewSet[HabilidadeUser]):
    queryset = HabilidadeUser.objects.all()
    serializer_class = HabilidadeUserSerializer

    def get_serializer_class(self) -> type[BaseSerializer[Any]]:
        if self.action == "multiplicar_xp":
            return MultiplicarXpSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=["post"], url_path="multiplicar-xp")
    def multiplicar_xp(self, request: Request, pk: int | None = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        habilidade = Habilidade.objects.get(
            id=serializer.validated_data["habilidade_id"]
        )
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
                status=status.HTTP_201_CREATED,
            )

        xp_para_upar = cast(int, habilidade_user.xp_para_upar)  # type: ignore

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

        return Response(status=status.HTTP_204_NO_CONTENT)

    @dataclass
    class _CalculoParametros:
        xp_atual: int
        lvl_atual: int
        multiplicador: float

    @dataclass
    class _CalculoResultado:
        xp: int
        nivel: int

    def _calcular_xp_para_upar(self, nivel: int) -> int:
        """Calcula a quantidade de XP necessária para upar para o próximo nível."""
        return 10 * (2 ** (nivel - 1))

    def _calcular(self, params: _CalculoParametros) -> _CalculoResultado:
        novo_xp = params.xp_atual * params.multiplicador
        novo_nivel = params.lvl_atual
        xp_para_upar = self._calcular_xp_para_upar(novo_nivel)

        while novo_xp >= xp_para_upar:
            novo_nivel += 1
            xp_para_upar = self._calcular_xp_para_upar(novo_nivel)

        return self._CalculoResultado(
            xp=int(novo_xp),
            nivel=novo_nivel,
        )
