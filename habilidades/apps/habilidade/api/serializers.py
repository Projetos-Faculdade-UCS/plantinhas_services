from apps.habilidade.models import HabilidadeUser, Habilidade

from rest_framework import serializers

class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidade
        fields = ["id", "nome"]

    def validate_nome(self, value):
        if not value:
            raise serializers.ValidationError("O nome da habilidade não pode ser vazio.")
        return value

class HabilidadeUserSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeSerializer()

    class Meta:
        model = HabilidadeUser
        fields = ["user_id", "habilidade", "xp", "nivel"]

    def validate_xp(self, value):
        if value < 0:
            raise serializers.ValidationError("XP não pode ser negativo.")
        if value > 10:
            raise serializers.ValidationError("XP não pode ser maior que 10.")
        return value
