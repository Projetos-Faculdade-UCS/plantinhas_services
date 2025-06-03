from apps.tutoriais.api.filters import PlantaFilter
from apps.tutoriais.api.serializers import CategoriaSerializer
from apps.tutoriais.api.serializers import PlantaSerializer
from apps.tutoriais.models import Categoria
from apps.tutoriais.models import Planta

from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend


class CategoriaViewSet(ModelViewSet[Categoria]):
    """
    API endpoint that allows categorias to be viewed or edited.
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PlantaViewSet(ModelViewSet[Planta]):
    """
    API endpoint that allows plantas to be viewed or edited.
    """

    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filterset_class = PlantaFilter
    filter_backends = [DjangoFilterBackend]
