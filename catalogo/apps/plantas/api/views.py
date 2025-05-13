from rest_framework.viewsets import ModelViewSet

from catalogo.apps.plantas.api.serializers import CategoriaSerializer
from catalogo.apps.plantas.api.serializers import PlantaSerializer
from catalogo.apps.plantas.models import Categoria
from catalogo.apps.plantas.models import Planta


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
