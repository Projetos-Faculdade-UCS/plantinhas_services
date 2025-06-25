from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Planta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    nome_cientifico = models.CharField(max_length=150, unique=True)
    foto = models.ImageField(upload_to="plantas/", blank=True, null=True)
    horas_sol = models.CharField(max_length=100)
    solo_ideal = models.CharField(max_length=100)
    ventilacao = models.CharField(max_length=100)
    temperatura_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    temperatura_ideal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    temperatura_maxima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in ºC",
    )
    estacao_plantio = models.CharField(max_length=100)
    dias_maturidade = models.IntegerField()
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="plantas"
    )
    dificuldade = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        help_text="Difficulty level from 1 to 5",
    )

    def __str__(self):
        return self.nome
