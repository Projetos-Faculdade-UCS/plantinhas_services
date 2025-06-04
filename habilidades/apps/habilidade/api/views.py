from rest_framework import viewsets
from habilidades.apps.habilidade.models import Habilidade
from apps.habilidade.api.serializers import HabilidadeSerializer


class HabilidadeViewSet(viewsets.ModelViewSet):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer

