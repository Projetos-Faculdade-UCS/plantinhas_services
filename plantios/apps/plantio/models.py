from django.db import models

class Plantio(models.Model):
    planta_id = models.IntegerField()
    user_id = models.IntegerField()
    data_plantio = models.DateField()
    data_prevista_colheita = models.DateField()
    saude = models.FloatField()
    sede = models.FloatField()
    situacao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.planta.nome} - {self.user.username}"