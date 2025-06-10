from __future__ import annotations

import datetime

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from tutoriais.models import Tutorial


class TarefaHabilidade(models.Model):
    habilidade_id: models.IntegerField[int, int] = models.IntegerField(
        verbose_name=_("Habilidade ID"),
        help_text=_("ID da habilidade associada à tarefa"),
    )
    multiplicador_xp: models.FloatField[float, float] = models.FloatField(
        default=1.0,
        validators=[
            validators.MinValueValidator(0.1),
            validators.MaxValueValidator(10.0),
        ],
        verbose_name=_("Multiplicador de XP"),
        help_text=_("Multiplicador de XP para a habilidade associada à tarefa"),
    )


class Tarefa(models.Model):
    TIPO_TAREFA_CHOICES = [
        ("recorrente", _("Recorrente")),
        ("pontual", _("Pontual")),
    ]

    nome: models.CharField[str, str] = models.CharField(
        max_length=200,
        verbose_name=_("Nome"),
    )
    tipo: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=TIPO_TAREFA_CHOICES,
        verbose_name=_("Tipo"),
    )
    quantidade_total: models.IntegerField[int, int] = models.IntegerField(
        verbose_name=_("Quantidade Total"),
    )
    quantidade_realizada: models.IntegerField[int, int] = models.IntegerField(
        default=0,
        verbose_name=_("Quantidade Realizada"),
        help_text=_("Quantidade de vezes que a tarefa foi realizada"),
    )
    atualizado_em: models.DateTimeField[datetime.datetime, datetime.datetime] = (
        models.DateTimeField(
            auto_now=True,
            verbose_name=_("Atualizado em"),
        )
    )
    cron: models.CharField[str, str] = models.CharField(
        max_length=100,
        verbose_name=_("Cron"),
        help_text=_("Formato Cron para agendamento"),
    )
    habilidade: models.ForeignKey["TarefaHabilidade", "TarefaHabilidade"] = (
        models.ForeignKey(
            "TarefaHabilidade",
            on_delete=models.CASCADE,
            related_name="tarefas",
            verbose_name=_("Habilidade"),
        )
    )
    tutorial: models.OneToOneField["Tutorial", "Tutorial"] = models.OneToOneField(
        "Tutorial",
        on_delete=models.CASCADE,
        related_name="tarefa",
        verbose_name=_("Tutorial"),
        null=True,  # Assuming a Tarefa might not always have a Tutorial
        blank=True,
    )
    criado_em: models.DateTimeField[datetime.datetime, datetime.datetime] = (
        models.DateTimeField(
            auto_now_add=True,
            verbose_name=_("Criado em"),
        )
    )
    concluida: models.BooleanField[bool, bool] = models.BooleanField(
        default=False, verbose_name=_("Concluída")
    )
    data_conclusao: models.DateTimeField[
        datetime.datetime | None, datetime.datetime | None
    ] = models.DateTimeField(null=True, blank=True, verbose_name=_("Data de Conclusão"))

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = _("Tarefa")
        verbose_name_plural = _("Tarefas")
        ordering = ["-criado_em"]
