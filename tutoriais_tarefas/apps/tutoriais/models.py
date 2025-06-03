from __future__ import annotations

import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Tutorial(models.Model):
    titulo: models.CharField[str, str] = models.CharField(
        max_length=200,
        verbose_name=_("Título"),
    )

    descricao: models.TextField[str, str] = models.TextField(
        verbose_name=_("Descrição"),
        blank=True,
    )

    criado_em: models.DateTimeField[datetime.datetime, datetime.datetime] = (
        models.DateTimeField(
            auto_now_add=True,
            verbose_name=_("Criado em"),
        )
    )

    atualizado_em: models.DateTimeField[datetime.datetime, datetime.datetime] = (
        models.DateTimeField(
            auto_now=True,
            verbose_name=_("Atualizado em"),
        )
    )

    def __str__(self) -> str:
        return self.titulo

    class Meta:
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutoriais")
        ordering = ["-criado_em"]


class MaterialTutorial(models.Model):
    tutorial: models.ForeignKey[Tutorial, Tutorial] = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
        related_name="materiais_tutorial",
        verbose_name=_("Tutorial"),
    )

    material: models.ForeignKey[Material, Material] = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="tutoriais_material",
        verbose_name=_("Material"),
    )

    quantidade: models.CharField[str, str] = models.CharField(
        max_length=50,
        verbose_name=_("Quantidade"),
        help_text=_("Ex: 1, 2 litros, 3 xícaras"),
    )

    def __str__(self) -> str:
        return f"{self.material.nome} - {self.quantidade}"

    class Meta:
        verbose_name = _("Material do Tutorial")
        verbose_name_plural = _("Materiais do Tutorial")
        unique_together = ["tutorial", "material"]


class Etapa(models.Model):
    tutorial: models.ForeignKey[Tutorial, Tutorial] = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
        related_name="etapas",
        verbose_name=_("Tutorial"),
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
        ordering = ["tutorial", "ordem"]
        unique_together = ["tutorial", "ordem"]
