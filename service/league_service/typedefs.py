from enum import Enum
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple


class LeagueServiceError(Exception):
    pass


class ServiceNotReadyError(LeagueServiceError):
    pass


PlayerID = int
RatingType = str  # e.g. "ladder_1v1"
Rating = Tuple[float, float]


class GameOutcome(Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"
    DRAW = "DRAW"
    MUTUAL_DRAW = "MUTUAL_DRAW"
    UNKNOWN = "UNKNOWN"
    CONFLICTING = "CONFLICTING"


class LeagueDivision(NamedTuple):
    id: int
    min_rating: float
    max_rating: float
    lowest_score: int
    highest_score: int


class League(NamedTuple):
    name: str
    divisions: List[LeagueDivision]
    current_season_id: int
    rating_type: str


class LeagueScore(NamedTuple):
    division_id: int
    score: int
    game_count: int


class LeagueRatingRequest(NamedTuple):
    """
    Minimal information to recalculate league score after a finished game.
    Includes a callback to acknowledge processing.
    """

    player_id: PlayerID
    rating_type: RatingType
    rating: Rating
    outcome: GameOutcome
    callback: Optional[Callable]

    @classmethod
    def from_rating_change_dict(cls, message: Dict):
        return cls(
            message["player_id"],
            message["rating_type"],
            (message["new_rating_mean"], message["new_rating_deviation"]),
            getattr(GameOutcome, message["outcome"]),
            message.get("_ack"),
        )
