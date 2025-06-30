from apps.plantio.api.pagination import CustomPagination
from apps.plantio.api.serializers import PlantioSerializer
from apps.plantio.models import Plantio

from rest_framework import viewsets


class PlantioViewSet(viewsets.ModelViewSet):
    queryset = Plantio.objects.all()
    serializer_class = PlantioSerializer
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = CustomPagination
