from __future__ import annotations

import datetime

from django.core import validators
from django.db import models
from django.db.models.lookups import GreaterThanOrEqual
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CronFrequencia(models.Model):
    cron_expression: "models.CharField[str, str]" = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Expressão Cron"),
        help_text=_("Expressão Cron para agendamento da tarefa"),
    )

    frequencia: "models.CharField[str, str]" = models.CharField(
        max_length=50,
        verbose_name=_("Frequência"),
        help_text=_(
            "Descrição da frequência da tarefa, ex: 'diária', 'semanal', 'mensal'"
        ),
    )


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
        ("cultivo", _("Cultivo")),
        ("colheita", _("Colheita")),
        ("irrigacao", _("Irrigação")),
        ("inspecao", _("Inspeção")),
        ("nutricao", _("Nutrição")),
        ("poda", _("Poda")),
    ]

    plantio_id: models.IntegerField[int, int] = models.IntegerField(
        verbose_name=_("Plantio ID"),
        help_text=_("ID do plantio associado à tarefa"),
    )

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
    criado_em: models.DateTimeField[datetime.datetime, datetime.datetime] = (
        models.DateTimeField(
            auto_now_add=True,
            verbose_name=_("Criado em"),
        )
    )
    concluida: models.GeneratedField = models.GeneratedField(
        expression=GreaterThanOrEqual(
            models.F("quantidade_realizada"), models.F("quantidade_total")
        ),  # type: ignore
        output_field=models.BooleanField(),  # type: ignore
        db_persist=True,
        verbose_name=_("Concluída"),
        help_text=_("Indica se a tarefa foi concluída"),
    )

    data_conclusao: models.DateTimeField[
        datetime.datetime | None, datetime.datetime | None
    ] = models.DateTimeField(null=True, blank=True, verbose_name=_("Data de Conclusão"))

    data_ultima_realizacao: models.DateTimeField[
        datetime.datetime | None, datetime.datetime | None
    ] = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Data da Última Realização"),
        help_text=_("Data e hora da última vez que a tarefa foi realizada"),
    )

    def __str__(self) -> str:
        return self.nome

    def realizar(self) -> None:
        """
        Marca a tarefa como realizada, atualizando a quantidade realizada e a data da última realização.
        Se a tarefa for concluída, também atualiza a data de conclusão.
        """
        self.quantidade_realizada += 1
        self.data_ultima_realizacao = timezone.now()

        if self.quantidade_realizada >= self.quantidade_total:
            self.concluida = True
            self.data_conclusao = timezone.now()

    class Meta:
        verbose_name = _("Tarefa")
        verbose_name_plural = _("Tarefas")
        ordering = ["-criado_em"]


class Material(models.Model):
    nome: models.CharField[str, str] = models.CharField(
        max_length=100,
        verbose_name=_("Nome"),
        unique=True,
    )

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materiais")
        ordering = ["nome"]


class MaterialTarefa(models.Model):
    tarefa: models.ForeignKey[Tarefa, Tarefa] = models.ForeignKey(
        Tarefa,
        on_delete=models.CASCADE,
        related_name="materiais",
        verbose_name=_("Tarefa"),
    )

    material: models.ForeignKey[Material, Material] = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="materiais_tarefa",
        verbose_name=_("Material"),
    )

    quantidade: models.DecimalField[float, float] = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Quantidade"),
        help_text=_("Ex: 1, 2, 3 (valor numérico)"),  # Updated help_text
    )

    unidade: models.CharField[str, str] = models.CharField(
        max_length=50,
        verbose_name=_("Unidade"),
        help_text=_("Ex: un, Litros, g"),
        default="un",  # Add a default if appropriate or allow blank=True
    )

    def __str__(self) -> str:
        return f"{self.material.nome} - {self.quantidade}"

    class Meta:
        verbose_name = _("Material da Tarefa")
        verbose_name_plural = _("Materiais da Tarefa")
        unique_together = ["tarefa", "material"]


class Etapa(models.Model):
    tarefa: models.ForeignKey[Tarefa, Tarefa] = models.ForeignKey(
        Tarefa,
        on_delete=models.CASCADE,
        related_name="etapas",
        verbose_name=_("Tarefa"),
    )

    descricao: models.TextField[str, str] = models.TextField(
        verbose_name=_("Descrição"),
    )

    ordem: models.PositiveIntegerField[int, int] = models.PositiveIntegerField(
        verbose_name=_("Ordem"),
        help_text=_("Ordem da etapa no processo"),
    )

    def __str__(self) -> str:
        return f"Etapa {self.ordem}: {self.descricao[:50]}..."

    class Meta:
        verbose_name = _("Etapa")
        verbose_name_plural = _("Etapas")
        ordering = ["tarefa", "ordem"]
        unique_together = ["tarefa", "ordem"]
