import logging
import os

# Logging setup
TRACE = 5
logging.addLevelName(TRACE, "TRACE")
logging.getLogger("aio_pika").setLevel(logging.INFO)

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3307))
DB_LOGIN = os.getenv("DB_LOGIN", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "banana")
DB_NAME = os.getenv("DB_NAME", "faf-league")

MQ_USER = os.getenv("MQ_USER", "faf-league-service")
MQ_PASSWORD = os.getenv("MQ_PASSWORD", "banana")
MQ_PORT = int(os.getenv("MQ_PORT", 5672))
MQ_VHOST = os.getenv("MQ_VHOST", "/faf-lobby")
MQ_PREFETCH_COUNT = int(os.getenv("MQ_PREFETCH_COUNT", 300))


EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "faf-rabbitmq")
LEAGUE_REQUEST_ROUTING_KEY = os.getenv(
    "LEAGUE_REQUEST_ROUTING_KEY", "success.gameResults.create"
)
LEAGUE_UPDATE_ROUTING_KEY = os.getenv(
    "LEAGUE_UPDATE_ROUTING_KEY", "success.rating.update"
)
LEAGUE_UPDATE_FAIL_ROUTING_KEY = os.getenv(
    "LEAGUE_UPDATE_FAIL_ROUTING_KEY", "failure.rating.update"
)

PLACEMENT_GAMES = int(os.getenv("PLACEMENT_GAMES", 10))
RATING_MODIFIER_FOR_PLACEMENT = int(os.getenv("RATING_MODIFIER_FOR_PLACEMENT", -300))
SCORE_GAIN = int(os.getenv("SCORE_GAIN", 1))
POSITIVE_BOOST = int(os.getenv("POSITIVE_BOOST", 1))
NEGATIVE_BOOST = int(os.getenv("NEGATIVE_BOOST", 1))
HIGHEST_DIVISION_BOOST = int(os.getenv("HIGHEST_DIVISION_BOOST", 1))
POINT_BUFFER_AFTER_DIVISION_CHANGE = int(
    os.getenv("POINT_BUFFER_AFTER_DIVISION_CHANGE", 2)
)
