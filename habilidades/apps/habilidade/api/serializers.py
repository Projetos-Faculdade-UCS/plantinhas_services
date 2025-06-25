from apps.habilidade.models import Habilidade

from rest_framework import serializers

class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidade
        fields = ["user_id", "nome", "xp", "nivel"]
