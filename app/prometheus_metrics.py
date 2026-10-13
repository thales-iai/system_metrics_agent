"""Exposition des métriques de l'agent au format Prometheus."""
from __future__ import annotations

from typing import Any

from prometheus_client import Gauge

CPU_PERCENT = Gauge("agent_cpu_percent", "Utilisation CPU (%)", ["hostname"])
MEMORY_PERCENT = Gauge("agent_memory_percent", "Utilisation RAM (%)", ["hostname"])
MEMORY_USED = Gauge("agent_memory_used_bytes", "RAM utilisée (octets)", ["hostname"])
MEMORY_TOTAL = Gauge("agent_memory_total_bytes", "RAM totale (octets)", ["hostname"])
LOAD_1M = Gauge("agent_load_1m", "Charge système sur 1 minute", ["hostname"])
LAST_SEEN = Gauge(
    "agent_last_received_timestamp_seconds",
    "Horodatage de la dernière métrique reçue",
    ["hostname"],
)


def update_gauges(data: dict[str, Any]) -> None:
    """Met à jour les jauges à partir du champ `data` d'une métrique reçue."""
    host = data.get("hostname", "unknown")
    CPU_PERCENT.labels(host).set(data["cpu"]["percent"])
    MEMORY_PERCENT.labels(host).set(data["memory"]["percent"])
    MEMORY_USED.labels(host).set(data["memory"]["used_bytes"])
    MEMORY_TOTAL.labels(host).set(data["memory"]["total_bytes"])
    load = data.get("system", {}).get("load_1m")
    if load is not None:
        LOAD_1M.labels(host).set(load)
    LAST_SEEN.labels(host).set_to_current_time()