from typing import Any
from typing import cast

from apps.plantas.api.filters import PlantaFilter
from apps.plantas.api.pagination import CustomPagination
from apps.plantas.api.pagination import PlantaPagination
from apps.plantas.api.serializers import CategoriaListSerializer
from apps.plantas.api.serializers import CategoriaSerializer
from apps.plantas.api.serializers import PlantaListSerializer
from apps.plantas.api.serializers import PlantaSerializer
from apps.plantas.api.serializers import SugestaoPlantaSerializer
from apps.plantas.models import Categoria
from apps.plantas.models import Planta

from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend


class CategoriaViewSet(ModelViewSet[Categoria]):
    """
    API endpoint that allows categorias to be viewed or edited.
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ["get"]
    pagination_class = CustomPagination

    def get_serializer_class(self):  # type: ignore
        """Return different serializers for list and detail views."""
        if self.action == "list":
            return CategoriaListSerializer
        return CategoriaSerializer

    @action(detail=True, methods=["get"])
    def plantas(
        self, request: Request, *args: list[Any], **kwargs: dict[str, Any]
    ) -> Response:
        """
        Returns a paginated list of all plantas in the categorias.
        """
        categorias = self.get_object()
        plantas = cast(QuerySet[Planta], categorias.plantas.all().order_by("nome"))  # type: ignore

        # Apply pagination
        paginator = PlantaPagination()
        page = paginator.paginate_queryset(plantas, request)
        if page is not None:
            serializer = PlantaListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)  # type: ignore

        # Fallback if pagination fails
        serializer = PlantaListSerializer(plantas, many=True)
        return Response(serializer.data)  # type: ignore


class PlantaViewSet(ModelViewSet[Planta]):
    """
    API endpoint that allows plantas to be viewed or edited.
    """

    queryset = Planta.objects.all().order_by("nome")
    serializer_class = PlantaSerializer
    pagination_class = PlantaPagination
    http_method_names = ["get"]
    filterset_class = PlantaFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):  # type: ignore
        """Return different serializers for list and detail views."""
        if self.action == "list":
            return PlantaListSerializer
        elif self.action == "sugerir":
            return SugestaoPlantaSerializer
        return PlantaSerializer

    @action(detail=False, methods=["post"])
    def sugerir(
        self, request: Request, *args: list[Any], **kwargs: dict[str, Any]
    ) -> Response:
        """
        Endpoint to suggest a new planta.
        """
        data = request.data.copy()
        data.update(
            {"usuario": request.user.id if request.user.is_authenticated else None}  # type: ignore
        )

        serializer = SugestaoPlantaSerializer(
            data=data,
        )  # type: ignore
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # type: ignore
        return Response(serializer.errors, status=400)  # type: ignore
