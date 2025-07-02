from apps.plantio.api.pagination import CustomPagination
from apps.plantio.api.serializers import PlantioSerializer
from apps.plantio.models import Plantio

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class PlantioViewSet(viewsets.ModelViewSet):
    queryset = Plantio.objects.all()
    serializer_class = PlantioSerializer
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Plantio.objects.filter(user_id=self.request.user.id).order_by(
            "-data_plantio"
        )
