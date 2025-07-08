from datetime import date
from datetime import datetime

from django.db import models


class Plantio(models.Model):
    planta_id: "models.IntegerField[int, int]" = models.IntegerField()
    user_id: "models.IntegerField[int, int]" = models.IntegerField()
    data_plantio: "models.DateField[date, date]" = models.DateField()
    data_prevista_colheita: "models.DateField[date, date]" = models.DateField()
    saude: "models.FloatField[float, float]" = models.FloatField()
    sede: "models.FloatField[float, float]" = models.FloatField()
    situacao: "models.CharField[str, str]" = models.CharField(max_length=100)
    informacoes_adicionais: "models.TextField[str, str]" = models.TextField(
        blank=True, null=True
    )
    data_atualizacao_saude: "models.DateTimeField[datetime, datetime]" = (
        models.DateTimeField(
            auto_now_add=True,
        )
    )
    data_atualizacao_sede: "models.DateTimeField[datetime, datetime]" = (
        models.DateTimeField(
            auto_now_add=True,
        )
    )

    def __str__(self):
        return f"{self.planta_id} - {self.user_id}"
