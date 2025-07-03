from dataclasses import dataclass
from typing import Any

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

        # Calcular XP e nível
        params = self._CalculoParametros(
            xp_atual=habilidade_user.xp,
            xp_para_upar=habilidade_user.xp_para_upar,
            lvl_atual=habilidade_user.nivel,
            multiplicador=multiplicador,
        )

        resultado = self._calcular(params)

        habilidade_user.xp = resultado.xp
        habilidade_user.nivel = resultado.nivel
        habilidade_user.xp_para_upar = resultado.novo_xp_para_upar

        habilidade_user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @dataclass
    class _CalculoParametros:
        xp_atual: int
        xp_para_upar: int
        lvl_atual: int
        multiplicador: float

    @dataclass
    class _CalculoResultado:
        xp: int
        nivel: int
        novo_xp_para_upar: int

    def _calcular(self, params: _CalculoParametros) -> _CalculoResultado:
        # TODO: Corrigir o cálculo de XP
        novo_xp = params.xp_atual * params.multiplicador
        novo_xp_aux = novo_xp
        count = 0

        while novo_xp_aux / 2 >= params.xp_para_upar:
            novo_xp_aux /= 2
            count += 1

        novo_nivel = params.lvl_atual + count
        if novo_nivel < 1:
            novo_nivel = 1

        novo_xp_para_upar = int(params.xp_para_upar * count * 2)
        if novo_xp_para_upar <= novo_xp:
            novo_xp_para_upar *= 2
        if novo_xp_para_upar == 0:
            novo_xp_para_upar = params.xp_para_upar

        return self._CalculoResultado(
            xp=int(novo_xp),
            nivel=novo_nivel,
            novo_xp_para_upar=novo_xp_para_upar,
        )
