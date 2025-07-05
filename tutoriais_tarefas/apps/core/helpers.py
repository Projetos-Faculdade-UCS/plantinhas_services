import re
from datetime import datetime

from apps.tarefas.models import CronFrequencia

import croniter


class CronHelper:
    """
    Helper class for handling cron expressions and their frequencies.
    """

    @staticmethod
    def get_data_proxima_ocorrencia(cron_expression: str) -> float | None:
        """
        Returns the next occurrence date based on the cron expression.
        If the cron expression is invalid or no next occurrence is found, returns None.
        """
        try:
            base_time = datetime.now()
            cron = croniter.croniter(cron_expression, base_time)
            return cron.get_next()
        except Exception:
            return None

    @staticmethod
    def get_data_ocorrencia_anterior(cron_expression: str) -> float | None:
        """
        Returns the previous occurrence date based on the cron expression.
        If the cron expression is invalid or no previous occurrence is found, returns None.
        """
        try:
            base_time = datetime.now()
            cron = croniter.croniter(cron_expression, base_time)
            return cron.get_prev()
        except Exception:
            return None

    @staticmethod
    def get_frequencia(cron_expression: str) -> str | None:
        """
        Returns the frequency description based on the cron expression.
        If no match is found, returns None.
        """
        cron_frequencias = CronFrequencia.objects.all()

        for cron_frequencia in cron_frequencias:
            regex = cron_frequencia.cron_expression
            descricao = cron_frequencia.frequencia
            match = re.match(regex, cron_expression)
            if match:
                # If the pattern has a format parameter, extract the interval value
                if "{0}" in descricao:
                    # Use named group 'interval' to get the interval value
                    interval = match.group("interval")
                    return descricao.format(interval)
                return descricao
        return None

    @staticmethod
    def pode_realizar_tarefa(
        cron_expression: str, ultima_realizacao: datetime | None
    ) -> bool:
        """
        Determines if the task can be concluded based on the cron expression.
        This is a placeholder method and should be implemented with actual logic.
        """

        data_ocorrencia_anterior = CronHelper.get_data_ocorrencia_anterior(
            cron_expression
        )
        if data_ocorrencia_anterior is None:
            return True

        if ultima_realizacao is None:
            return True

        ultima_realizacao_ts = ultima_realizacao.timestamp()

        return ultima_realizacao_ts < data_ocorrencia_anterior
