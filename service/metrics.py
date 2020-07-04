from prometheus_client import Gauge

league_service_backlog = Gauge(
    "league_service_backlog", "Number of games remaining to be rated"
)
