from apps.plantio.models import Plantio

from rest_framework import serializers


class PlantioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantio
        fields = [
            "id",
            "planta_id",
            "situacao",
            "saude",
            "sede",
            "data_plantio",
            "data_prevista_colheita",
            "informacoes_adicionais",
        ]
