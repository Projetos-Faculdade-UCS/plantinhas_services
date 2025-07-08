from apps.plantio.api.pagination import CustomPagination
from apps.plantio.api.serializers import PlantioSerializer
from apps.plantio.models import Plantio

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer


class PlantioViewSet(viewsets.ModelViewSet):  # type: ignore
    queryset = Plantio.objects.all()
    serializer_class = PlantioSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id  # type: ignore
        return Plantio.objects.filter(user_id=user_id).order_by("-data_plantio")

    def perform_create(  # type: ignore
        self, serializer: BaseSerializer[Plantio]
    ) -> None:
        user_id = self.request.user.id  # type: ignore
        serializer.save(user_id=user_id)
