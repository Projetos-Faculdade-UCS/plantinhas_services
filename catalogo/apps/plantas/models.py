from datetime import datetime

from django.db import models


class Categoria(models.Model):
    nome: "models.CharField[str, str]" = models.CharField(max_length=100, unique=True)
    descricao: "models.TextField[str, str]" = models.TextField()

    def __str__(self):
        return self.nome


class Planta(models.Model):
    nome: "models.CharField[str, str]" = models.CharField(max_length=100, unique=True)
    nome_cientifico: "models.CharField[str, str]" = models.CharField(
        max_length=150, unique=True
    )
    foto = models.ImageField(upload_to="plantas/", blank=True, null=True)
    horas_sol: "models.CharField[str, str]" = models.CharField(max_length=100)
    solo_ideal: "models.CharField[str, str]" = models.CharField(max_length=100)
    ventilacao: "models.CharField[str, str]" = models.CharField(max_length=100)
    temperatura_minima: "models.DecimalField[float, float]" = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    temperatura_ideal: "models.DecimalField[float, float]" = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    temperatura_maxima: "models.DecimalField[float, float]" = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    estacao_plantio: "models.CharField[str, str]" = models.CharField(max_length=100)
    dias_maturidade: "models.IntegerField[int, int]" = models.IntegerField()
    categoria: "models.ForeignKey[Categoria, Categoria]" = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="plantas"
    )
    dificuldade: "models.DecimalField[float, float]" = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        help_text="Difficulty level from 1 to 5",
    )

    def __str__(self):
        return self.nome


class SugestaoPlanta(models.Model):
    planta_sugerida: "models.CharField[str, str]" = models.CharField(max_length=100)
    usuario: "models.IntegerField[int, int]" = models.IntegerField()
    data_criacao: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Sugestão de {self.usuario} para {self.planta_sugerida}"
