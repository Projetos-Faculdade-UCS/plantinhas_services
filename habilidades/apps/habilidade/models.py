from decimal import Decimal

from django.db import models


class Habilidade(models.Model):
    nome: "models.CharField[str, str]" = models.CharField(max_length=50)
    descricao: "models.TextField[str, str]" = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class HabilidadeUser(models.Model):
    user_id: "models.IntegerField[int, int]" = models.IntegerField()
    habilidade: "models.OneToOneField[Habilidade, Habilidade]" = models.OneToOneField(
        Habilidade, on_delete=models.CASCADE
    )
    xp: "models.DecimalField[float | Decimal, Decimal]" = models.DecimalField(
        default=1,
        max_digits=10,
        decimal_places=2,
    )
    nivel: "models.IntegerField[int, int]" = models.IntegerField(default=1)
    xp_para_upar: "models.GeneratedField" = models.GeneratedField(
        expression=(models.F("nivel") * 30) - 20,
        db_persist=True,
        output_field=models.IntegerField(),
    )
    porcentagem: "models.GeneratedField" = models.GeneratedField(
        expression=models.F("xp") / (models.F("nivel") * 30 - 20) * 100,
        db_persist=True,
        output_field=models.DecimalField(max_digits=5, decimal_places=2),
    )

    class Meta:
        unique_together = ("user_id", "habilidade")

    def __str__(self):
        return f"{self.user_id} - {self.habilidade.nome} (XP: {self.xp}, Nível: {self.nivel})"
