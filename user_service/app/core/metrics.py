"""
Модуль для сбора метрик с помощью Prometheus.
Определены счетчики и гистограммы для мониторинга количества запросов и задержек.
"""

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("user_service_requests_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("user_service_request_latency_seconds", "Request latency in seconds", ["endpoint"])

def setup_metrics() -> None:
    """
    Заглушка для инициализации метрик, если потребуется дополнительная настройка.
    """
    pass