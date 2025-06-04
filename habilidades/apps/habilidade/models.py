from django.db import models

class Habilidade(models.Model):
    user_id = models.IntegerField()
    nome = models.CharField(max_length=20)
    xp = models.IntegerField(editable=False)
    nivel = models.IntegerField()

    