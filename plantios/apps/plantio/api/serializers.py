from apps.plantio.models import Plantio

from rest_framework import serializers

class PlantioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantio
        fields = ["planta_id", "user_id", "data_plantio", "data_prevista_colheita", "saude", "sede", "situacao"]
