from django.db import models

class Habilidade(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class HabilidadeUser(models.Model):
    user_id = models.IntegerField()
    habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    xp = models.IntegerField()
    nivel = models.IntegerField()

    class Meta:
        unique_together = ('user_id', 'habilidade')

    def __str__(self):
        return f"{self.user_id} - {self.habilidade.nome} (XP: {self.xp}, Nível: {self.nivel})"