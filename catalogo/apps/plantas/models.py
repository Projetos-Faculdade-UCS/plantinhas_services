from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Planta(models.Model):
    nome = models.CharField(max_length=100)
    nome_cientifico = models.CharField(max_length=150)
    foto = models.ImageField(upload_to="plantas/", blank=True, null=True)
    horas_sol = models.CharField(max_length=100)
    solo_ideal = models.CharField(max_length=100)
    ventilacao = models.CharField(max_length=100)
    temperatura_ideal = models.CharField(max_length=100)
    estacao_plantio = models.CharField(max_length=100)
    dias_maturidade = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    dificuldade = models.IntegerField()

    def __str__(self):
        return self.nome
