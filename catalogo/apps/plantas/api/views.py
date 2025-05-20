from apps.plantas.api.filters import PlantaFilter
from apps.plantas.api.serializers import CategoriaSerializer
from apps.plantas.api.serializers import PlantaSerializer
from apps.plantas.models import Categoria
from apps.plantas.models import Planta

from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend


class CategoriaViewSet(ModelViewSet):
    """
    API endpoint that allows categorias to be viewed or edited.
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PlantaViewSet(ModelViewSet):
    """
    API endpoint that allows plantas to be viewed or edited.
    """

    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filterset_class = PlantaFilter
    filter_backends = [DjangoFilterBackend]
