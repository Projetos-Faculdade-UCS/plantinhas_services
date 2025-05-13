from apps.plantas.models import Categoria
from apps.plantas.models import Planta

from rest_framework import serializers


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome", "descricao"]
        read_only_fields = ["id"]
        extra_kwargs = {"nome": {"required": True}, "descricao": {"required": True}}


class PlantaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()

    class Meta:
        model = Planta
        fields = [
            "id",
            "nome",
            "nome_cientifico",
            "foto",
            "horas_sol",
            "solo_ideal",
            "ventilacao",
            "temperatura_ideal",
            "estacao_plantio",
            "dias_maturidade",
            "dificuldade",
            "categoria",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "nome": {"required": True},
            "nome_cientifico": {"required": True},
            "horas_sol": {"required": True},
            "solo_ideal": {"required": True},
            "ventilacao": {"required": True},
            "temperatura_ideal": {"required": True},
            "estacao_plantio": {"required": True},
            "dias_maturidade": {"required": True},
            "dificuldade": {"required": True},
        }

    def create(self, validated_data):
        """Isto é feito somente quando tem um campo relacionado com outro serializer."""
        categoria_data = validated_data.pop("categoria")
        nome_categoria = categoria_data.get("nome")
        # If the category exists (by nome), get it; otherwise create it
        categoria_instance, created = Categoria.objects.get_or_create(
            nome=nome_categoria, defaults=categoria_data
        )
        planta_instance = Planta.objects.create(
            categoria=categoria_instance, **validated_data
        )
        return planta_instance

    def update(self, instance, validated_data):
        """Isto é feito somente quando tem um campo relacionado com outro serializer."""
        if "categoria" in validated_data:
            categoria_data = validated_data.pop("categoria")
            nome_categoria = categoria_data.get("nome")
            # If the category exists (by nome), get it; otherwise create it
            categoria_instance, created = Categoria.objects.get_or_create(
                nome=nome_categoria, defaults=categoria_data
            )
            instance.categoria = categoria_instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
