from django.db import models
from django.db.models.functions import Power


class Habilidade(models.Model):
    nome: "models.CharField[str, str]" = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class HabilidadeUser(models.Model):
    user_id: "models.IntegerField[int, int]" = models.IntegerField()
    habilidade: "models.ForeignKey[Habilidade, Habilidade]" = models.ForeignKey(
        Habilidade, on_delete=models.CASCADE
    )
    xp: "models.IntegerField[int, int]" = models.IntegerField(default=1)
    nivel: "models.IntegerField[int, int]" = models.IntegerField(default=1)
    xp_para_upar: "models.GeneratedField" = models.GeneratedField(
        expression=10 * Power(2, models.F("nivel") - 1),
        db_persist=True,
        output_field=models.IntegerField(),
    )

    class Meta:
        unique_together = ("user_id", "habilidade")

    def __str__(self):
        return f"{self.user_id} - {self.habilidade.nome} (XP: {self.xp}, Nível: {self.nivel})"
