from django.db import models


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    concluida = models.BooleanField(default=False, verbose_name="Concluída")
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_conclusao = models.DateTimeField(
        null=True, blank=True, verbose_name="Data de Conclusão"
    )

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ["-data_criacao"]

    def __str__(self):
        return self.titulo
