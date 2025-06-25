from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.habilidade.models import HabilidadeUser
from apps.habilidade.api.serializers import HabilidadeUserSerializer


class HabilidadeViewSet(viewsets.ModelViewSet):
    queryset = HabilidadeUser.objects.all()
    serializer_class = HabilidadeUserSerializer

    @action(detail=True, methods=["post"], url_path="aumentar-nivel")
    def aumentar_nivel(self, request, pk=None):
        habilidade = self.get_object()
        habilidade.xp += 1
        if habilidade.xp >= 10:
            habilidade.nivel += 1
            habilidade.xp = 0
        habilidade.save()
        serializer = self.get_serializer(habilidade)
        return Response(serializer.data, status=status.HTTP_200_OK)

