from apps.plantas.api.filters import PlantaFilter
from apps.plantas.api.pagination import CustomPagination
from apps.plantas.api.pagination import PlantaPagination
from apps.plantas.api.serializers import CategoriaListSerializer
from apps.plantas.api.serializers import CategoriaSerializer
from apps.plantas.api.serializers import PlantaListSerializer
from apps.plantas.api.serializers import PlantaSerializer
from apps.plantas.models import Categoria
from apps.plantas.models import Planta

from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend


class CategoriaViewSet(ModelViewSet[Categoria]):
    """
    API endpoint that allows categorias to be viewed or edited.
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = CustomPagination

    def get_serializer_class(self):  # type: ignore
        """Return different serializers for list and detail views."""
        if self.action == "list":
            return CategoriaListSerializer
        return CategoriaSerializer


class PlantaViewSet(ModelViewSet[Planta]):
    """
    API endpoint that allows plantas to be viewed or edited.
    """

    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    pagination_class = PlantaPagination
    http_method_names = ["get", "post", "put", "delete"]
    filterset_class = PlantaFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):  # type: ignore
        """Return different serializers for list and detail views."""
        if self.action == "list":
            return PlantaListSerializer
        return PlantaSerializer
