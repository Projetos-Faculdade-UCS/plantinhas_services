from math import ceil
from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """Custom pagination class that returns pagination data in the specified format."""

    page_size = 10
    page_size_query_param = "itensPorPagina"
    page_query_param = "pagina"
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        """Return a paginated style Response."""
        if not self.page:  # type: ignore
            return Response(
                {
                    "total": 0,
                    "itensPorPagina": self.page_size,
                    "paginaAtual": 1,
                    "ultimaPagina": 1,
                    "itens": data,
                }
            )

        total_pages = ceil(self.page.paginator.count / (self.page_size or 10))  # type: ignore

        return Response(
            {
                "total": self.page.paginator.count,  # type: ignore
                "itensPorPagina": self.page_size or 10,
                "paginaAtual": self.page.number,  # type: ignore
                "ultimaPagina": total_pages,
                "itens": data,
            }
        )

    def get_page_size(self, request: Any) -> int:
        """Get the page size for the current request."""
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0:
                    max_size = self.max_page_size or 100
                    calculated_size = min(page_size, max_size)
                    self.page_size = calculated_size
                    return calculated_size
            except (KeyError, ValueError):
                pass
        return self.page_size or 10
