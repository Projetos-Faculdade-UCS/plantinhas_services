from django.db import models


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
    xp_para_upar: "models.IntegerField[int, int]" = models.IntegerField(default=10)

    class Meta:
        unique_together = ("user_id", "habilidade")

    def __str__(self):
        return f"{self.user_id} - {self.habilidade.nome} (XP: {self.xp}, Nível: {self.nivel})"
