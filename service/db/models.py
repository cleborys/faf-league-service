from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

login = Table(
    "login",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("ip", String),
    Column("steamid", Integer, unique=True),
    Column("create_time", TIMESTAMP, nullable=False),
    Column("update_time", TIMESTAMP, nullable=False),
    Column("user_agent", String),
    Column("last_login", TIMESTAMP),
)

leaderboard = Table(
    "leaderboard",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("technical_name", String, nullable=False, unique=True),
)

league = Table(
    "league",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("technical_name", String, nullable=False, unique=True),
)

league_season = Table(
    "league_season",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("league_id", Integer, ForeignKey("league.id")),
    Column("leaderboard_id", Integer, ForeignKey("leaderboard.id")),
    Column("start_date", TIMESTAMP),
    Column("end_date", TIMESTAMP),
)

league_season_division = Table(
    "league_season_division",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("league_season_id", Integer, ForeignKey("league_season.id")),
    Column("division_index", Integer),
    Column("min_rating", Float),
    Column("max_rating", Float),
    Column("highest_score", Integer),
)

league_season_score = Table(
    "league_season_score",
    metadata,
    Column("login_id", Integer, ForeignKey("login.id")),
    Column("league_season_id", Integer, ForeignKey("league_season.id")),
    Column("division_id", Integer, ForeignKey("league_season_division.id")),
    Column("score", Integer),
    Column("game_count", Integer),
)
