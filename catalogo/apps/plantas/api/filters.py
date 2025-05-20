from apps.plantas.models import Planta

from django.db.models import Q

from django_filters import CharFilter
from django_filters import FilterSet


class PlantaFilter(FilterSet):
    search = CharFilter(
        method="filter_search",
        label="Buscar",
        help_text="Buscar por nome ou nome científico",
        field_name="search",
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nome__icontains=value) | Q(nome_cientifico__icontains=value)
        )

    class Meta:
        model = Planta
        fields = {}
